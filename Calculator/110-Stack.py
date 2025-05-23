from collections import deque


class Lexer:
    EOF = '?'
    def __init__(self, src):
        self.queue = deque(src)

    @staticmethod
    def is_operator(token):
        return token in '+-*/()'

    @staticmethod
    def is_space(token):
        return token in ' \t\n'

    def push_number(self):
        nums = ''
        while (self.queue and not Lexer.is_space(self.queue[0])
               and not self.is_operator(self.queue[0])):
            nums += self.queue.popleft()
        self.queue.appendleft(float(nums))

    def peek_token(self):
        try:
            while self.queue[0] in ' \t\n':
                self.queue.popleft()
        except IndexError:
            return Lexer.EOF
        token = self.queue[0]
        if Lexer.is_operator(token):
            return token
        elif isinstance(token, float):
            return token
        else:
            self.push_number()
            return self.queue[0]

    def get_token(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return Lexer.EOF


def to_postfix(src):
    is_op = lambda t: t in '+-*/'
    is_lparen = lambda t: t == '('
    is_rparen = lambda t: t == ')'
    is_op_multi_divide = lambda t: t in '*/'

    lexer = Lexer(src)
    op_stack = []
    postfix_queue = []
    token = lexer.peek_token()
    while token != Lexer.EOF:
        if isinstance(token, float):
            postfix_queue.append(lexer.get_token())
        elif is_lparen(token):
            op_stack.append(lexer.get_token())
        elif is_rparen(token):
            while op_stack and not is_lparen(op_stack[-1]):
                postfix_queue.append(op_stack.pop())
            op_stack.pop()
            lexer.get_token()
        elif is_op(token):
            if is_op_multi_divide(token):
                while op_stack and is_op_multi_divide(op_stack[-1]):
                    postfix_queue.append(op_stack.pop())
            else:
                while op_stack and is_op(op_stack[-1]):
                    postfix_queue.append(op_stack.pop())
            op_stack.append(lexer.get_token())
        token = lexer.peek_token()
    if op_stack:
        postfix_queue.append(op_stack.pop())
    return postfix_queue


def calc_infix(op, left, right):
    if op == '+':
        return left + right
    elif op == '-':
        return left - right
    elif op == '/':
        return left / right
    elif op == '*':
        return left * right
    else:
        raise ValueError('Invalid operator')


def eval_postfix(postfix_queue):
    is_op = lambda t: t in '+-*/'
    operands = []
    for token in postfix_queue:
        if isinstance(token, float):
            operands.append(token)
        elif is_op(token):
            right = operands.pop()
            left = operands.pop()
            operands.append(calc_infix(token, left, right))
    return operands.pop()


class Node:
    def __init__(self, data, left=None, right=None):
        self.data, self.left, self.right = data, left, right

    def prefix(self):
        op = self.data
        left = f' {self.left.prefix()}' if self.left else ''
        right = f' {self.right.prefix()}' if self.right else ''
        return f'{op}{left}{right}'

    def infix(self):
        left = f'{self.left.infix()} ' if self.left else ''
        op = self.data
        right = f' {self.right.infix()}' if self.right else ''
        if left:
            return f'({left}{op}{right})'
        else:
            return f'{op}'


    def postfix(self):
        left = f'{self.left.postfix()} ' if self.left else ''
        right = f'{self.right.postfix()} ' if self.right else ''
        op = self.data
        return f'{left}{right}{op}'


class ExpressionTree:
    def __init__(self, postfix_queue):
        nodes = []
        for token in postfix_queue:
            if isinstance(token, float):
                nodes.append(Node(token))
            else:
                right = nodes.pop()
                left = nodes.pop()
                nodes.append(Node(token, left, right))
        self.root = nodes.pop()

    def prefix(self):
        return self.root.prefix()

    def infix(self):
        return self.root.infix()

    def postfix(self):
        return self.root.postfix()

def calc(src):
    print(src)
    postfix_queue = to_postfix(src)
    tree = ExpressionTree(postfix_queue)
    print('Prefix :', tree.prefix())
    print('Infix  :', tree.infix())
    print('Postfix:', tree.postfix())
    value = eval_postfix(postfix_queue)
    return value


if __name__ == '__main__':
    src = '((1+3)*((1-3)-2 - (3+5))+(3/(2-3)))'
    val = calc(src)
    print(val)
