from collections import deque


class Lexer:
    EOF = 'EOF'
    def __init__(self, exp):
        self.tokens = self.tokenize(exp)

    def tokenize(self, exp):
        tokens = deque()
        for ch in list(exp):
            if ch in ' \t\n': continue
            tokens.append(ch)
        tokens.append(Lexer.EOF)
        return tokens

    def get_token(self):
        return self.tokens.popleft()
