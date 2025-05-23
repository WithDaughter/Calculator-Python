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
        else:
            return self.lexer.get_token()

    def term(self):
        left = self.get_factor()
        while self.lexer.peek_token() == '*' or self.lexer.peek_token() == '/':
            op = self.lexer.get_token()
            right = self.get_factor()
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
