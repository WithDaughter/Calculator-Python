from Lexer import Lexer
from Parser import Parser


def calc(exp):
    lexer = Lexer(exp)
    parser = Parser(lexer)
    val = parser.expression()
    return val


if __name__ == '__main__':
    exp = '1.23*2-0.46+(0.1*3)'
    val = calc(exp)
    print(val)