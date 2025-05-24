import pytest

from python.lisp.lis import *


# @pytest.mark.skip
def test_check_tokens_error():
    with pytest.raises(ValueError):
        assert check_syntax('3 + 1') == ['3', '+', '1']


@pytest.mark.parametrize(
    'input_, expected',
    [
        ('3', ['3']),
        ('  3   ', ['3']),
        ('(2)', ['(', '2', ')']),
        ('( 2     )', ['(', '2', ')']),
        ('(+2 3)', ['(', '+2', '3', ')']),
        ('(+ 2 3)', ['(', '+', '2', '3', ')']),
        ('(define (abc x y) (+ x y))',
                ['(', 'define', '(', 'abc', 'x', 'y', ')',
          '(', '+', 'x', 'y', ')', ')']),
    ])
def test_tokenize(input_, expected):
    assert tokenize(input_) == expected


def test_check_tokens_tokens_raise():
    with pytest.raises(ValueError):
        assert check_syntax('1 + 2') == [1, '+', 2]


def test_read_tokens_raise():
    with pytest.raises(IndexError):
        assert read([]) == []


def test_read_tokens_rparen_raise():
    with pytest.raises(SyntaxError):
        assert read([')']) == []


def test_read_tokens_rparen_raise_error():
    with (pytest.raises(IndexError)):
        assert read(['(', 'define', '(', 'abc', 'x', 'y', ')',
                       '(', '+', 'x', 'y', ')']
                    ) == ['define', ['abc', 'x', 'y'], ['+', 'x', 'y']]


@pytest.mark.parametrize(
    'input_, expected',
    [
        (['3'], 3),
        (['3.14'], 3.14),
        (['314.1592e-2'], 3.141592),
        (['abc'], 'abc'),
        (['3', '+', '4'], 3),
        (['(', ')'], []),
        (['(', '3', '+', '4', ')'], [3, '+', 4]),
        (['(', '+2', '3', ')'], [2, 3]),
        (['(', '-2', '3', ')'], [-2, 3]),
        (['(', '+', '2', '3', ')'], ['+', 2, 3]),
        (['(', 'define', '(', 'abc', 'x', 'y', ')',
                '(', '+', 'x', 'y', ')', ')'],
            ['define', ['abc', 'x', 'y'], ['+', 'x', 'y']]),
    ])
def test_read_tokens(input_, expected):
    assert read(input_) == expected

@pytest.mark.parametrize(
    'input_, expected',
    [
        (3, '3'),
        (3.14, '3.14'),
        (314.1592e-2, '3.141592'),
        ('abc', 'abc'),
        (['3', '+', '4'], '(3 + 4)'),
        ([], '()'),
        (['3', '+', '4'], '(3 + 4)'),
        (['+', '2', '3'], '(+ 2 3)'),
        (['2', '3'], '(2 3)'),
        (['-2', '3'], '(-2 3)'),
        (['define', ['abc', 'x', 'y'],
                ['+', 'x', 'y']],
            '(define (abc x y) (+ x y))'),
    ])
def test_lisp_str(input_, expected):
    assert lisp_str(input_) == expected

# @pytest.mark.parametrize(
#     'program, expected',
#     [
#         ('3', '3'),
#         ('(define temp 100)', '100'),
#         ('temp', 100),
#     ]
# )
# def test_evaluate(program, expected):
#     global_env = Environment({}, default_env())
#     tokens = tokenize(program)
#     exp = read_tokens(tokens)
#     val = evaluate(exp, global_env)
#     if val is not None:
#         assert lisp_str(val) == expected
