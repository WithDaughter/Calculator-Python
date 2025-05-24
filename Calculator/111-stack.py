from collections import deque

from tables import node
from tenacity import retry_unless_exception_type

EOF = '~'
OPERATOR = '+-*/()'
OPERATOR4 = '+-*/'
LPAREN = '('
RPAREN = ')'
MULTIPLY_OR_DIVIDE = '*/'
PLUS_OR_MINUS = '+-'
NUMBER = '0123456789'


class Lexer:
    def __init__(self, src):
        self.tokens = deque(src)

    def get_token(self):
        SPACES = ' \t\n\r\f\v'
        if not self.tokens: return EOF
        token = self.tokens.popleft()
        while self.tokens and token in SPACES:
            token = self.tokens.popleft()
        if token in SPACES: return EOF
        if token in OPERATOR:
            return token
        elif token in NUMBER:
            nums = token
            while self.tokens and self.tokens[0] in NUMBER:
                nums += self.tokens.popleft()
            if self.tokens and self.tokens[0] == '.':
                nums += self.tokens.popleft()
                while self.tokens and self.tokens[0] in NUMBER:
                    nums += self.tokens.popleft()
            return nums
        else:
            raise SyntaxError('unexpected token')


def to_post(src):
    lexer = Lexer(src)
    queue = []
    stack = []
    while (token := lexer.get_token()) != EOF:
        if token in ' \t\n': continue
        if token in OPERATOR:
            if token == LPAREN:
                stack.append(token)
            elif token == RPAREN:
                while stack and stack[-1] != LPAREN:
                    queue.append(stack.pop())
                stack.pop()
            elif token in MULTIPLY_OR_DIVIDE:
                while stack and stack[-1] in MULTIPLY_OR_DIVIDE:
                    queue.append(stack.pop())
                stack.append(token)
            elif token in PLUS_OR_MINUS:
                while stack and stack[-1] in OPERATOR4:
                    queue.append(stack.pop())
                stack.append(token)
        else:
            queue.append(token)
    while stack:
        queue.append(stack.pop())
    return queue


def calc_infix(token, left, right):
    if token == '+':
        return left + right
    elif token == '-':
        return left - right
    elif token == '*':
        return left * right
    elif token == '/':
        return left / right
    else:
        raise Exception('Invalid token')


def eval_post(tokens):
    stack = []
    for token in tokens:
        if token in OPERATOR4:
            right = stack.pop()
            left = stack.pop()
            stack.append(calc_infix(token, float(left), float(right)))
        else:
            stack.append(token)
    return stack.pop()


class Node:
    def __init__(self, data, left = None, right = None):
        self.data, self.left, self.right = data, left, right

    def postfix(self):
        left = self.left.postfix() if self.left else ''
        right = self.right.postfix() if self.right else ''
        op = self.data
        return f'{left+" " if left else ""}{right+" " if right else ""}{op}'

    def infix(self):
        left = self.left.infix() if self.left else ''
        op = self.data
        right = self.right.infix() if self.right else ''
        return f'({left} {op} {right})' if left else f'{op}'

    def prefix(self):
        op = self.data
        left = self.left.prefix() if self.left else ''
        right = self.right.prefix() if self.right else ''
        return f'{op}{" "+left if left else ""}{" "+right if right else ""}'


class ExpressionTree:
    def __init__(self, tokens):
        self.tokens = deque(tokens)
        self.root = self.make_root()

    def make_root(self):
        nodes = []
        for token in self.tokens:
            if token in OPERATOR:
                right = nodes.pop()
                left = nodes.pop()
                nodes.append(Node(token, left, right))
            else:
                nodes.append(Node(token))
        return nodes.pop()

    def print_postfix(self):
        return self.root.postfix()

    def print_infix(self):
        return self.root.infix()

    def print_prefix(self):
        return self.root.prefix()


def calc(src):
    print('source :', src)
    tokens = to_post(src)
    tree = ExpressionTree(tokens)
    print('prefix :', tree.print_prefix())
    print('infix  :', tree.print_infix())
    print('postfix:', tree.print_postfix())
    val = eval_post(tokens)
    return val


def main():
    # src = '(2-5)*2'
    # src = '2.5*2 + 3.5-0.5'
    src = '(1 - 2) * 3 / 4 + 7'
    print(calc(src))


if __name__ == '__main__':
    main()