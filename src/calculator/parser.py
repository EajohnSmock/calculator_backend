from decimal import Decimal, InvalidOperation


class CalculatorError(ValueError):
    """Base exception for invalid calculator expressions."""


class InvalidExpressionError(CalculatorError):
    """Raised when the expression does not follow the calculator grammar."""


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is requested."""


def tokenize(expression):
    """Convert a string expression into number/operator/parenthesis tokens."""
    tokens = []
    index = 0

    while index < len(expression):
        char = expression[index]

        if char.isspace():
            index += 1
            continue

        if char.isdigit() or char == '.':
            start = index
            dot_count = 0

            while index < len(expression):
                current = expression[index]

                if current.isdigit():
                    index += 1
                    continue

                if current == '.':
                    dot_count += 1

                    if dot_count > 1:
                        raise InvalidExpressionError(
                            'Invalid number format'
                        )

                    index += 1
                    continue

                break

            number_text = expression[start:index]

            if number_text == '.':
                raise InvalidExpressionError(
                    'Invalid number format'
                )

            try:
                Decimal(number_text)
            except InvalidOperation as error:
                raise InvalidExpressionError(
                    'Invalid number format'
                ) from error

            tokens.append(('NUMBER', number_text))
            continue

        if char in '+-*/()':
            tokens.append((char, char))
            index += 1
            continue

        raise InvalidExpressionError(
            f'Invalid character: {char}'
        )

    if not tokens:
        raise InvalidExpressionError('Expression is empty')

    tokens.append(('EOF', 'EOF'))
    return tokens


class Parser:
    """
    Recursive-descent parser.

    Grammar:
        expression -> term ((+ | -) term)*
        term       -> unary ((* | /) unary)*
        unary      -> (+ | -) unary | primary
        primary    -> NUMBER | '(' expression ')'
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    @property
    def current(self):
        return self.tokens[self.position]

    def consume(self, token_type):
        if self.current[0] != token_type:
            raise InvalidExpressionError('Invalid expression')

        token = self.current
        self.position += 1
        return token

    def parse(self):
        value = self.parse_expression()

        if self.current[0] != 'EOF':
            raise InvalidExpressionError('Invalid expression')

        return value

    def parse_expression(self):
        value = self.parse_term()

        while self.current[0] in ('+', '-'):
            operator = self.current[0]
            self.consume(operator)
            right = self.parse_term()

            if operator == '+':
                value += right
            else:
                value -= right

        return value

    def parse_term(self):
        value = self.parse_unary()

        while self.current[0] in ('*', '/'):
            operator = self.current[0]
            self.consume(operator)
            right = self.parse_unary()

            if operator == '*':
                value *= right
            else:
                if right == 0:
                    raise DivisionByZeroError(
                        'Division by zero is not allowed'
                    )
                value /= right

        return value

    def parse_unary(self):
        if self.current[0] == '+':
            self.consume('+')
            return self.parse_unary()

        if self.current[0] == '-':
            self.consume('-')
            return -self.parse_unary()

        return self.parse_primary()

    def parse_primary(self):
        if self.current[0] == 'NUMBER':
            number_text = self.consume('NUMBER')[1]
            return Decimal(number_text)

        if self.current[0] == '(':
            self.consume('(')
            value = self.parse_expression()
            self.consume(')')
            return value

        raise InvalidExpressionError('Invalid expression')


def evaluate_expression(expression):
    tokens = tokenize(expression)
    parser = Parser(tokens)
    return parser.parse()


def format_decimal(value):
    """Convert Decimal to a clean calculator display string."""
    if value == 0:
        return '0'

    normalized = value.normalize()
    text = format(normalized, 'f')

    if '.' in text:
        text = text.rstrip('0').rstrip('.')

    return text
