import time
import re
from collections import deque

start_time = time.time()


def load_data():
    with open('day_eighteen_data_sample.txt') as fh:
        data = [re.sub(r'\n|\s', '', line) for line in fh.readlines()]
    return data


class Token:

    def __init__(self, value):
        self.value = value

    @property
    def PATTERN(self):
        raise NotImplementedError

    def __repr__(self):
        return f'{self.__class__.__name__}-{self.value}'

    @classmethod
    def eval(cls):
        raise Exception(f"Can't evaluate {cls__name__}")

    @classmethod
    def matches(cls, raw_string):
        return re.match(cls.PATTERN, raw_string)

    @classmethod
    def chomp(cls, raw_string):
        matches = re.match(cls.PATTERN, raw_string)
        if matches:
            start, end = matches.span()
            return cls(raw_string[start:end]), raw_string[end:]


class Number(Token):
    PATTERN = r'\d+'

    def eval(self):
        return int(self.value)


class Operator(Token):
    PATTERN = r'\+|\*|/|-'


class LeftParenthesis(Token):
    PATTERN = r'\('


class RightParenthesis(Token):
    PATTERN = r'\)'


def get_tokens(raw_string):
    tokens = []
    while len(raw_string) > 0:
        for TokenType in [Number, LeftParenthesis, RightParenthesis, Operator]:
            if TokenType.matches(raw_string):
                token, raw_string = TokenType.chomp(raw_string)
                tokens.append(token)
    return tokens


class TokenGroup:

    def __init__(self, tokens):
        self.tokens = tokens


class ParenthesisGroup(TokenGroup):
    def __repr__(self):
        return 'Paren(' + ''.join(repr(token) for token in self.tokens) + ')'

    @classmethod
    def chomp_tokens(cls, tokens):
        count_parentheses = 1
        loc = 1
        while count_parentheses > 0:
            if isinstance(tokens[loc], LeftParenthesis):
                count_parentheses += 1
            elif isinstance(tokens[loc], RightParenthesis):
                count_parentheses -= 1
            loc += 1
        return cls(parse_tokens(tokens[1:loc-1])), tokens[loc:]

    def eval(self):
        return self.tokens[0].eval()


class Bop(TokenGroup):
    @classmethod
    def chomp_tokens(cls, tokens, left):
        operator, *remaining_tokens = tokens
        right, remaining_tokens = Factor.chomp_tokens(remaining_tokens)
        return cls([left, operator, right]), remaining_tokens

    def __init__(self, tokens):
        super().__init__(tokens)
        self.left, self.operator, self.right = tokens

    def __repr__(self):
        return f'Bop({self.left} {self.operator} {self.right})'

    def eval(self):
        if self.operator.value == '+':
            return self.left.eval() + self.right.eval()
        elif self.operator.value == '*':
            return self.left.eval() * self.right.eval()


class Factor(TokenGroup):
    """Number or parenthesis"""
    @classmethod
    def chomp_tokens(cls, tokens):
        token = tokens[0]
        if isinstance(token, Number):
            return token, tokens[1:]
        elif isinstance(token, LeftParenthesis):
            return ParenthesisGroup.chomp_tokens(tokens)


def parse_tokens(tokens):
    stack = deque()
    token_id = 0
    remaining_tokens = tokens
    while remaining_tokens:
        token = remaining_tokens[0]
        if isinstance(token, (Number, LeftParenthesis)):
            token, remaining_tokens = Factor.chomp_tokens(tokens)
            stack.append(token)
        elif isinstance(token, Operator):
            left = stack.pop()
            node, remaining_tokens = Bop.chomp_tokens(remaining_tokens, left)
            stack.append(node)
    return stack


data = load_data()

total = 0
for example in data:
    tokens = get_tokens(example)
    ast = parse_tokens(tokens)
    root = ast[0]
    # print(root)
    # print(root.eval())
    total += root.eval()
print(total)
print("--- %s seconds ---" % (time.time() - start_time))


class Bop(TokenGroup):
    @classmethod
    def chomp_tokens(cls, tokens, left):
        operator, *remaining_tokens = tokens
        right, remaining_tokens = Factor.chomp_tokens(remaining_tokens)
        if remaining_tokens and remaining_tokens[0].value == '+':
            next, remaining_tokens = Bop.chomp_tokens(remaining_tokens, right)
            return cls([left, operator, next]), remaining_tokens
        return cls([left, operator, right]), remaining_tokens

    def __init__(self, tokens):
        super().__init__(tokens)
        self.left, self.operator, self.right = tokens

    def __repr__(self):
        return f'Bop({self.left} {self.operator} {self.right})'

    def eval(self):
        if self.operator.value == '+':
            return self.left.eval() + self.right.eval()
        elif self.operator.value == '*':
            return self.left.eval() * self.right.eval()


data = load_data()

total = 0
for example in data:
    tokens = get_tokens(example)
    ast = parse_tokens(tokens)
    root = ast[0]
    total += root.eval()
print(total)

print("--- %s seconds ---" % (time.time() - start_time))
