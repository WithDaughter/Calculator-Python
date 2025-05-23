from Lexer import Lexer
from Parser import Parser


def calc(exp):
    lexer = Lexer(exp)
    parser = Parser(lexer)
    val = parser.expression()
    return val


if __name__ == '__main__':
    exp = '2*5 + 3*2- 1'
    val = calc(exp)
    print(val)