from constants import *


class Token:
    def __init__(self, token):
        self.token = token


class Symbol(Token):
    token_type = TokenType.SYMBOL
    pass


class Keyword(Token):
    token_type = TokenType.KEYWORD
    pass


class Identifier(Token):
    token_type = TokenType.IDENTIFIER
    pass


class Constant(Token):
    pass


class IntegerConstant(Token):
    token_type = TokenType.INT_CONST

    def __init__(self, token):
        Token.__init__(self, token)
        self.token = int(token)


class StringConstant(Token):
    token_type = TokenType.STRING_CONST
