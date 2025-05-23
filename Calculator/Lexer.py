from collections import deque


class Lexer:
    def __init__(self, exp):
        self.tokens = self.tokenize(exp)

    def tokenize(self, exp):
        tokens = deque(list(exp))
        return tokens

    def get_token(self):
        return self.tokens.popleft()
