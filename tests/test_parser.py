import pytest

from src.calculator.parser import (
    DivisionByZeroError,
    InvalidExpressionError,
    evaluate_expression,
    format_decimal,
)


@pytest.mark.parametrize(
    ('expression', 'expected'),
    [
        ('12+8', '20'),
        ('10-3', '7'),
        ('5*6', '30'),
        ('20/4', '5'),
        ('2.5+1.5', '4'),
        ('1+2*3', '7'),
        ('(1+2)*3', '9'),
        ('10/2+7', '12'),
        ('8-3*2', '2'),
        ('-5+8', '3'),
        ('3*-2', '-6'),
        ('3*+2', '6'),
        ('-(2+3)', '-5'),
        ('0.1+0.2', '0.3'),
    ],
)
def test_valid_expressions(expression, expected):
    result = evaluate_expression(expression)
    assert format_decimal(result) == expected


@pytest.mark.parametrize(
    'expression',
    [
        '',
        '1+',
        '(1+2',
        '1+2)',
        '1..2+3',
        'abc+1',
        '2**3',
        '()',
    ],
)
def test_invalid_expressions(expression):
    with pytest.raises(InvalidExpressionError):
        evaluate_expression(expression)


def test_division_by_zero():
    with pytest.raises(DivisionByZeroError):
        evaluate_expression('5/0')
