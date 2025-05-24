import math


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def get_factor(self):
        if self.lexer.peek_token() == '(':
            self.lexer.get_token()
            val = self.expression()
            if self.lexer.get_token() != ')':
                raise SyntaxError(')가 없습니다.')
            return val
        elif self.lexer.peek_token() == '-':
            self.lexer.get_token()
            val = self.lexer.get_token()
            return -val
        else:
            return self.lexer.get_token()

    def get_secondary(self):
        left = self.get_factor()
        while self.lexer.peek_token() == '**':
            op = self.lexer.get_token()
            right = self.get_factor()
            left = math.pow(left, right)
        return left

    def term(self):
        left = self.get_secondary()
        while self.lexer.peek_token() == '*' or self.lexer.peek_token() == '/':
            op = self.lexer.get_token()
            right = self.get_secondary()
            if op == '*':
                left *= right
            else:
                left /= right
        return left

    def expression(self):
        left = self.term()
        while self.lexer.peek_token() == '+' or self.lexer.peek_token() == '-':
            op = self.lexer.get_token()
            right = self.term()
            if op == '+':
                left += right
            else:
                left -= right
        return left
