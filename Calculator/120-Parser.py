from Lexer import Lexer
from Parser import Parser


def calc(exp):
    lexer = Lexer(exp)
    parser = Parser(lexer)
    val = parser.plus()
    return val


if __name__ == '__main__':
    exp = '3 + 2'
    val = calc(exp)
    print(val)