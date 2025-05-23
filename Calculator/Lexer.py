from collections import deque


class Lexer:
    EOF = 'EOF'
    def __init__(self, exp):
        self.tokens = self.tokenize(exp)

    def tokenize(self, exp):
        tokens = deque()
        for ch in list(exp):
            if ch in ' \t\n': continue
            if ch in '+-*/()':
                tokens.append(ch)
            else:
                tokens.append(int(ch))
        tokens.append(Lexer.EOF)
        return tokens

    def peek_token(self):
        return self.tokens[0]

    def get_token(self):
        return self.tokens.popleft()
