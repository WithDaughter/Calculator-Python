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
        num = self.exp[self.cursor]
        while (self.cursor + 1 < len(self.exp)
                and Lexer.is_number(self.exp[self.cursor + 1])):
            self.cursor += 1
            num += self.exp[self.cursor]
        return int(num)

    def tokenize(self):
        while self.cursor < len(self.exp):
            ch = self.exp[self.cursor]
            if ch in ' \t\n':
                pass
            elif ch in '+-*/()':
                self.tokens.append(ch)
            elif Lexer.is_number(ch):
                self.tokens.append(self.get_number())
            self.cursor += 1
        self.tokens.append(Lexer.EOF)

    def peek_token(self):
        return self.tokens[0]

    def get_token(self):
        return self.tokens.popleft()
