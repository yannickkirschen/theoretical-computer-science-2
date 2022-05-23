import math
import re


class Stack:
    def __init__(self):
        self._elements = []

    def push(self, e):
        self._elements.append(e)

    def pop(self):
        assert len(self._elements) > 0, "popping empty stack"
        self._elements = self._elements[:-1]

    def top(self):
        assert len(self._elements) > 0, "top of empty stack"
        return self._elements[-1]

    def is_empty(self):
        return self._elements == []

    def copy(self):
        c = Stack()
        c._elements = self._elements[:]
        return c

    def __str__(self):
        c = self.copy()
        result = c._convert()
        return result

    def _convert(self):
        if self.is_empty():
            return '|'
        t = self.top()
        self.pop()
        return self._convert() + ' ' + str(t) + ' |'


def create_stack(from_list):
    s = Stack()
    n = len(from_list)
    for i in range(n):
        s.push(from_list[i])
    return s


def find_zero(f, a, b, n):
    assert a < b, f'{a} has to be less than b'
    assert f(a) * f(b) <= 0, f'f({a}) * f({b}) > 0'

    if f(a) <= 0 <= f(b):
        for k in range(n):
            c = 0.5 * (a + b)

            if f(c) < 0:
                a = c
            elif f(c) > 0:
                b = c
            else:
                return c
    else:
        for k in range(n):
            c = 0.5 * (a + b)

            if f(c) > 0:
                a = c
            elif f(c) < 0:
                b = c
            else:
                return c

    return (a + b) / 2


def is_white_space(s):
    return re.compile(r'[ \t]+').fullmatch(s)


def to_float(s):
    try:
        return float(s)
    except ValueError:
        return s


def tokenize(s):
    regex = r'''
              0|[1-9][0-9]* |             # number
              \*\*          |             # power operator
              [-+*/()]      |             # arithmetic operators and parentheses
              [ \t]         |             # white space
              sqrt          |
              sin           |
              cos           |
              tan           |   
              asin          |
              acos          |
              atan          |
              exp           |
              log           |
              x             |
              e             |
              pi
              '''
    return list(reversed([to_float(t) for t in re.findall(regex, s, flags=re.VERBOSE) if not is_white_space(t)]))


def precedence(op):
    if op in ('+', '-'):
        return 1

    if op in ('*', '/'):
        return 2

    if op == '**':
        return 3

    if op in ('sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'sqrt', 'exp'):
        return 4

    if op in ('x', 'e', 'pi'):
        return 5


def is_unary_operator(op):
    return op in ('sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'sqrt', 'exp')


def is_const_operator(op):
    return op in ('x', 'e', 'pi')


def is_left_associative(op):
    if op in ('+', '-', '*', '/'):
        return True

    if op in ('**', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'sqrt', 'exp'):
        return False

    assert False, f'unknown operator {op}'


def eval_before(stack_op, next_op):
    if precedence(stack_op) > precedence(next_op):
        return True

    if stack_op == next_op and not is_unary_operator(stack_op):
        return is_left_associative(stack_op)

    if is_unary_operator(stack_op) and is_unary_operator(next_op):
        return False

    if stack_op != next_op \
            and precedence(stack_op) == precedence(next_op) \
            and not is_unary_operator(stack_op):
        return True

    if precedence(stack_op) < precedence(next_op):
        return False

    assert False, f'incomplete case distinction in evalBefore({stack_op}, {next_op})'


class Calculator:
    def __init__(self, tl, x=0):
        self._tokens = create_stack(tl)
        self._operators = Stack()
        self._arguments = Stack()
        self._x_value = x

    def evaluate(self):
        while not self._tokens.is_empty():
            next_op = self._tokens.top()
            self._tokens.pop()

            if isinstance(next_op, float):
                self._arguments.push(next_op)
            elif self._operators.is_empty():
                self._operators.push(next_op)
            elif next_op == '(':
                self._operators.push(next_op)
            elif next_op == ')' and self._operators.top() == '(':
                self._operators.pop()
            elif next_op == ')' and self._operators.top() != '(':
                self.pop_and_evaluate()
                self._tokens.push(next_op)
            elif next_op != ')' and self._operators.top() == '(':
                self._operators.push(next_op)
            elif eval_before(self._operators.top(), next_op):
                self.pop_and_evaluate()
                self._tokens.push(next_op)
            else:
                self._operators.push(next_op)

        while not self._operators.is_empty():
            self.pop_and_evaluate()

        return self._arguments.top()

    def pop_and_evaluate(self):
        op = self._operators.top()
        self._operators.pop()

        result = None

        if is_unary_operator(op):
            arg = self._arguments.top()
            self._arguments.pop()

            if op == 'sin':
                result = math.sin(arg)
            elif op == 'cos':
                result = math.cos(arg)
            elif op == 'tan':
                result = math.tan(arg)
            elif op == 'asin':
                result = math.asin(arg)
            elif op == 'acos':
                result = math.acos(arg)
            elif op == 'atan':
                result = math.atan(arg)
            elif op == 'log':
                result = math.log(arg)
            elif op == 'sqrt':
                result = math.sqrt(arg)
            elif op == 'exp':
                result = math.exp(arg)
        elif is_const_operator(op):
            if op == 'pi':
                result = math.pi
            elif op == 'e':
                result = math.e
            elif op == 'x':
                result = self._x_value
        else:
            rhs = self._arguments.top()
            self._arguments.pop()

            lhs = self._arguments.top()
            self._arguments.pop()

            if op == '+':
                result = lhs + rhs
            elif op == '-':
                result = lhs - rhs
            elif op == '*':
                result = lhs * rhs
            elif op == '/':
                result = lhs / rhs
            elif op == '**':
                result = lhs ** rhs

        assert result is not None, f'ERROR: *** Unknown Operator *** "{op}"'
        self._arguments.push(result)

    def __str__(self):
        return '\n'.join(['_' * 50,
                          'TokenStack: ', str(self._tokens),
                          'Arguments:  ', str(self._arguments),
                          'Operators:  ', str(self._operators),
                          '_' * 50])


def test_evaluate_expr(s, t, x):
    c = Calculator(tokenize(s), x)
    r1 = c.evaluate()
    r2 = eval(t, {'math': math}, {'x': x})
    assert r1 == r2, f'{r1} != {r2}'


def compute_zero(s, left, right):
    def f(x):
        c = Calculator(tokenize(s), x)
        return c.evaluate()

    return find_zero(f, left, right, 54)


test_evaluate_expr('sin cos x', 'math.sin(math.cos(x))', 0)
test_evaluate_expr('sin x**2', 'math.sin(math.pi)**2', math.pi)
test_evaluate_expr('log e ** x + 1 * 2 - 3', 'math.log(math.e**x) + 1 * 2 - 3 ', 1)

zero = compute_zero('log exp x - cos(sqrt(x**2))', 0, 1)
print(zero)
