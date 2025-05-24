from collections import deque


def parse_number(src):
    '''숫자 만들기
    123 = 1*10*10 + 2*10 + 3*1 (3 x 10^0)
    0.123 = 1*0.1 + 2*0.01 + 3*0.001
    '''
    ch2num = lambda n: ord(n) - ord('0')
    num = 0
    while src and (n := peek_token(src)) in '0123456789':
        get_token(src)
        num *= 10
        num += ch2num(n)
    if (n := peek_token(src)) != '.':
        return num

    get_token(src)
    weight = 1
    while src and (n := peek_token(src)) in '0123456789':
        get_token(src)
        weight /= 10
        weight *= ch2num(n)
    return num + weight


def peek_token(src):
    if not src:
        return None
    t = src[0]
    while t in ' \t\n':
        src.popleft()
        t = src[0]
    return t


def get_token(src):
    if not src:
        raise IndexError('src에 값이 없습니다')
    t = src.popleft()
    if t in ' \t\n':
        t = get_token(src)
    return t


def eval_factor(src):
    factor = peek_token(src)
    if factor in '0123456789':
        return parse_number(src)
    elif factor == '(':
        get_token(src)
        value = eval_exp(src)
        get_token(src)
        return value
    else:
        raise ValueError('숫자가 아닙니다')


def eval_term(src):
    left = eval_factor(src)
    while src and ((op := peek_token(src)) == '*' or op == '/'):
        get_token(src)
        right = eval_factor(src)
        if op == '*':
            left *= right
        else:
            left /= right
    return left


def eval_exp(src):
    left = eval_term(src)
    while src and ((op := peek_token(src)) == '+' or op == '-'):
        get_token(src)
        right = eval_term(src)
        if op == '+':
            left += right
        else:
            left -= right
    return left


def eval_source(src):
    result = eval_exp(src)
    if src:
        raise SyntaxError('수식의 끝에 불필요한 내용이 있습니다.')
    return result


def main():
    # src = deque('2+3')
    # src = deque('1*3*2+3*4*5+4') # 70
    # src = deque('2-3-4') # -5
    # src = deque('2-6/3') # -5
    # src = deque('2-(6/3-2)-(1+1)') # 2
    # src = deque('(100 + (30 - 7))-8 + 4565')
    # src = deque('123.5')
    # src = deque('(123 + 0.5) - (1 / 2)')
    while True:
        src = input('> ')
        print(eval_source(deque(src)))


if __name__ == '__main__':
    main()