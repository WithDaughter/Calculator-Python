# http://norvig.com/lispy.html
from collections import ChainMap
from itertools import chain


def tokenize(program):
    '''입력 string => 토큰 리스트
    '(+ 1 2)' => ['(', '+', '1', '2', ')']
    '''
    return program.replace('(', ' ( ').replace(')', ' ) ').split()


def eval_atom(token):
    '''숫자 => 숫자, string => symbol'''
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)


def parse(tokens):
    '''Tokens => Abstract Syntax Tree
    ['(', '+', '1', '2', ')'] => ['+', 1, 2]
    '''
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if token == '(':
        arr = []
        while tokens and tokens[0] != ')':
            arr.append(parse(tokens))
        tokens.pop(0)
        return arr
    elif token == ')':
        raise SyntaxError('느닷없이 ) ?')
    else:
        return eval_atom(token)


def read():
    prompt = '계산> '
    program = input(prompt)
    return parse(tokenize(program))
    # tokens = tokenize(program)
    # return parse(tokens)


class Environment(ChainMap):

    def set(self, key, value):
        for map in self.maps:
            if key in map:
                map[key] = value
                return
        raise KeyError(key)


def global_env():
    import operator as op
    import math
    env = Environment()
    env.update(vars(math))
    env.update({
        '+': lambda *args: sum(args),
        '-': lambda first, *rest: first - sum(rest) if rest else -first,
        '*': lambda *args: math.prod(args),
        '/': lambda first, *rest: first / math.prod(rest) if rest else 1 / first,
        '//': op.floordiv, '**': op.pow, '%': op.mod,
        '<': op.lt, '>': op.gt, '<=': op.le, '>=': op.ge,
        '==': op.eq, '!=': op.ne, 'is': op.is_, 'not': op.not_,
        'abs': abs, 'max': max, 'min': min, 'sum': sum, 'round': round,
        'cons': lambda x, y: [x] + y,
        'true': True, 'false': False,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'empty?': lambda x: x == [],
        'first': lambda x: x[0],
        'rest': lambda x: x[1:],
        'print': lambda x: print(lisp_str(x)),
        'number?': lambda x: isinstance(x, (int, float)),
        'symbol?': lambda x: isinstance(x, str),
        'function?': callable,
        'length': len,
        'append': lambda *args: list(chain(*args)),
        'apply': lambda func, args: func(*args),
        'filter': lambda *args: list(filter(*args)),
        'map': lambda *args: list(map(*args)),
        # 'begin': lambda *x: x[-1],
    })
    return env


class Function:

    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def function_env(self, args):
        local_env = dict(zip(self.params, args))
        return Environment(local_env, self.env)

    def __call__(self, *args):
        env = self.function_env(args)
        for exp in self.body:
            res = eval_(exp, env)
        return res


def cond_form(clauses, env):
    for clause in clauses:
        match clause:
            case ['else', *body]:
                for exp in body:
                    res = eval_(exp, env)
                return res
            case [test, *body] if eval_(test, env):
                for exp in body:
                    res = eval_(exp, env)
                return res
    return


def or_form(exps, env):
    val = False
    for exp in exps:
        val = eval_(exp, env)
        if val:
            return True
    return val


def and_form(exps, env):
    val = True
    for exp in exps:
        val = eval_(exp, env)
        if not val:
            return False
    return val


KEYWORDS = ['quote', 'if', 'let', '=', 'lambda', 'define',
            'cond', 'or', 'and', 'begin']

TCO_ENABLED = True
def eval_(exp, env):
    '''AST 계산 in Environment
    ['+', 1, 2] => 3
    '''
    while True:
        match exp:
            case int(x) | float(x):
                return x
            case str(symbol):
                try:
                    return env[symbol]
                except KeyError as exc:
                    raise KeyError(symbol) from exc
            case ['quote', x]:
                return x
            case ['if', test, then, alt]:
                if eval_(test, env):
                    exp = eval_(then, env)
                else:
                    exp = eval_(alt, env)
            case ['let', str(name), val]:
                env[name] = eval_(val, env)
                return env[name]
            case ['=', str(name), val]:
                env.set(name, eval_(val, env))
                return env[name]
            case ['lambda', [*params], *body] if body:
                return Function(params, body, env)
            case ['def', [str(func_name), *params], *body] if body:
                env[func_name] = Function(params, body, env)
                return
            case ['cond', *clauses]:
                return cond_form(clauses, env)
            case ['or', *exps]:
                return or_form(exps, env)
            case ['and', *exps]:
                return and_form(exps, env);
            case ['begin', *exps]:
                for exp in exps[:-1]:
                    eval_(exp, env)
                exp = exps[-1]
            case [str(func_name), *args] if func_name not in KEYWORDS:
                func = eval_(func_name, env)
                args_ = [eval_(arg, env) for arg in args]
                if TCO_ENABLED and isinstance(func, Function):
                    exp = ['begin', *func.body]
                    env = func.function_env(args_)
                else:
                    try:
                        return func(*args_)
                    except TypeError as exc:
                        msg = (f'{exc!r}\ninvoking: {func!r}({args!r}):'
                               f'\nsource: {lisp_str(exp)}\nAST: {exp!r}')
                        raise TypeError(msg) from exc
            case _:
                raise SyntaxError('계산식 오류')


def lisp_str(value):
    if isinstance(value, list):
        return f'({' '.join(map(lisp_str, value))})'
    else:
        return str(value)


def repl(env):
    ast = read()
    value = eval_(ast, env)
    if value is not None:
        print(lisp_str(value))


def run(source):
    env = Environment({}, global_env())
    tokens = tokenize(source)
    while tokens:
        exp = parse(tokens)
        result = eval_(exp, env)
    return result


def main(args):
    if len(args) == 1:
        with open(args[0]) as fp:
            run(fp.read())
    else:
        env = Environment({}, global_env())
        while True:
            try:
                repl(env)
            except EOFError:
                break
            except Exception as e:
                print(f'에러: {e}')


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
