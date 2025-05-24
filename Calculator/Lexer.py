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
        while self.is_number(self.peek_char()):
            self.next_char()
            num += self.get_char()
        if self.peek_char() != '.':
            return int(num)
        self.next_char()
        num += self.get_char()
        while self.is_number(self.peek_char()):
            self.next_char()
            num += self.get_char()
        return float(num)

    def get_asterisk(self):
        asterisk = self.get_char()
        if self.peek_char() == '*':
            self.next_char()
            asterisk += self.get_char()
        return asterisk

    def peek_char(self):
        if self.cursor + 1 < len(self.exp):
            return self.exp[self.cursor + 1]
        return Lexer.EOF

    def get_char(self):
        return self.exp[self.cursor]

    def next_char(self):
        self.cursor += 1

    def tokenize(self):
        while self.cursor < len(self.exp):
            ch = self.get_char()
            if ch in ' \t\n':
                pass
            elif ch in '+-/()':
                self.tokens.append(ch)
            elif ch == '*':
                self.tokens.append(self.get_asterisk())
            elif Lexer.is_number(ch):
                self.tokens.append(self.get_number())
            self.next_char()
        self.tokens.append(Lexer.EOF)

    def peek_token(self):
        return self.tokens[0]

    def get_token(self):
        return self.tokens.popleft()
