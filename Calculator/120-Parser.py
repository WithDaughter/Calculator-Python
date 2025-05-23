from Lexer import Lexer
from Parser import Parser


def calc(exp):
    lexer = Lexer(exp)
    parser = Parser(lexer)
    val = parser.expression()
    return val


if __name__ == '__main__':
    exp = '1+2*3'
    val = calc(exp)
    print(val)