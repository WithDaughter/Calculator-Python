from Lexer import Lexer


def get_literal(lexer):
    return lexer.get_token()

def plus(lexer):
    left = get_literal(lexer)
    if lexer.peek_token() == '+':
        op = lexer.get_token()
        right = get_literal(lexer)
        left += right
    return left


def calc(exp):
    lexer = Lexer(exp)
    val = plus(lexer)
    return val


if __name__ == '__main__':
    exp = '3+2'
    val = calc(exp)
    print(val)