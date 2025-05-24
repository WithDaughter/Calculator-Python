from functools import reduce


def to_float(str):
    return float(str)


def stripped(str):
    return str.strip()


def divide(exp):
    arr = exp.split('/')
    strip_arr = map(stripped, arr)
    init = to_float(next(strip_arr))
    return reduce(lambda acc, cur: acc / cur, map(to_float, strip_arr), init)


def multiply(exp):
    arr = exp.split('*')
    strip_arr = map(stripped, arr)
    return reduce(lambda acc, cur: acc * cur, map(divide, strip_arr), 1)


def minus(exp):
    arr = exp.split('-')
    strip_arr = map(stripped, arr)
    init = multiply(next(strip_arr))
    return reduce(lambda acc, cur: acc - cur, map(multiply, strip_arr), init)


def plus(exp):
    arr = exp.split('+')
    strip_arr = map(stripped, arr)
    return reduce(lambda acc, cur: acc + cur , map(minus, strip_arr), 0)


def parenthesis(exp):
    if '(' in exp:
        start = exp.index('(')
        changed = parenthesis(exp[start + 1:])
        return parenthesis(exp[0:start] + changed)
    elif ')' in exp:
        end = exp.index(')')
        return str(plus(exp[:end])) + exp[end + 1:]
    else:
        return exp


def eval(exp):
    return plus(parenthesis(exp))


def main():
    exp = '1+(1 + 1)+ 22 - (2*3) +1'
    print(eval(exp))


if __name__ == '__main__':
    main()