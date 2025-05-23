from Lexer import Lexer


def calc(exp):
    lexer = Lexer(exp)
    # val = lexer.get_token()
    while (val := lexer.get_token()) != Lexer.EOF:
        print(val)
    return val


if __name__ == '__main__':
    exp = '1+2'
    val = calc(exp)
    print(val)