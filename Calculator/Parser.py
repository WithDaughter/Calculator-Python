class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def get_literal(self):
        return self.lexer.get_token()

    def plus(self):
        left = self.get_literal()
        while self.lexer.peek_token() == '+':
            op = self.lexer.get_token()
            right = self.get_literal()
            left += right
        return left
