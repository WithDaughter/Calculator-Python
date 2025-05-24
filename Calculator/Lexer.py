from collections import deque


class Lexer:
    EOF = 'EOF'
    def __init__(self, exp):
        self.exp = list(exp)
        self.cursor = 0
        self.tokens = deque()
        self.tokenize()

    @staticmethod
    def is_number(ch):
        return ch in '0123456789'

    def get_number(self):
        num = self.get_char()
        while Lexer.is_number(self.peek_char()):
            num += self.get_char()
        if self.peek_char() != '.':
            return int(num)
        num += self.get_char()
        while Lexer.is_number(self.peek_char()):
            num += self.get_char()
        return float(num)

    def get_asterisk(self):
        asterisk = self.get_char()
        if self.peek_char() == '*':
            asterisk += self.get_char()
        return asterisk

    def peek_char(self):
        if self.cursor == len(self.exp):
            return Lexer.EOF
        return self.exp[self.cursor]

    def get_char(self):
        ch = self.peek_char()
        if self.cursor < len(self.exp):
            self.cursor += 1
        return ch

    def tokenize(self):
        while self.cursor < len(self.exp):
            ch = self.peek_char()
            if ch in ' \t\n':
                self.get_char()
            elif ch in '+-/()':
                self.tokens.append(self.get_char())
            elif ch == '*':
                self.tokens.append(self.get_asterisk())
            elif Lexer.is_number(ch):
                self.tokens.append(self.get_number())

    def peek_token(self):
        if self.tokens:
            return self.tokens[0]
        return Lexer.EOF

    def get_token(self):
        return self.tokens.popleft()
