import re
from token import *


class TokenType:
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4
    KEYWORD = 5
    COMMENT_START = 6
    COMMENT_END = 6


class Tokens:
    CLASS = Keyword('class')
    METHOD = Keyword('method')
    FUNCTION = Keyword('function')
    CONSTRUCTOR = Keyword('constructor')
    INT = Keyword('int')
    BOOLEAN = Keyword('boolean')
    CHAR = Keyword('char')
    VOID = Keyword('void')
    VAR = Keyword('var')
    STATIC = Keyword('static')
    FIELD = Keyword('field')
    LET = Keyword('let')
    DO = Keyword('do')
    IF = Keyword('if')
    ELSE = Keyword('else')
    WHILE = Keyword('while')
    RETURN = Keyword('return')
    TRUE = Keyword('true')
    FALSE = Keyword('false')
    NULL = Keyword('null')
    THIS = Keyword('this')

    LEFT_CURLY_BRACKET = Symbol('{')
    RIGHT_CURLY_BRACKET = Symbol('}')
    LEFT_ROUND_BRACKET = Symbol('(')
    RIGHT_ROUND_BRACKET = Symbol(')')
    LEFT_BOX_BRACKET = Symbol('[')
    RIGHT_BOX_BRACKET = Symbol(']')
    DOT = Symbol('.')
    COMMA = Symbol(',')
    SEMI_COLON = Symbol(';')
    PLUS = Symbol('+')
    MINUS = Symbol('-')
    MULTI = Symbol('*')
    DIV = Symbol('/')
    AND = Symbol('&')
    PIPE = Symbol('|')
    LESS_THAN = Symbol('<')
    GREATER_THAN = Symbol('>')
    EQUAL = Symbol('=')
    TILDE = Symbol('~')

class TokenMap:
    KEYWORDS = {
        'class': Tokens.CLASS,
        'constructor': Tokens.CONSTRUCTOR,
        'function': Tokens.FUNCTION,
        'method': Tokens.METHOD,
        'field': Tokens.FIELD,
        'static': Tokens.STATIC,
        'var': Tokens.VAR,
        'int': Tokens.INT,
        'char': Tokens.CHAR,
        'boolean': Tokens.BOOLEAN,
        'void': Tokens.VOID,
        'true': Tokens.TRUE,
        'false': Tokens.FALSE,
        'null': Tokens.NULL,
        'this': Tokens.THIS,
        'let': Tokens.LET,
        'do': Tokens.DO,
        'if': Tokens.IF,
        'else': Tokens.ELSE,
        'while': Tokens.WHILE,
        'return': Tokens.RETURN
    }

    SYMBOLS = {
        '{': Tokens.LEFT_CURLY_BRACKET,
        '}': Tokens.RIGHT_CURLY_BRACKET,
        '(': Tokens.LEFT_ROUND_BRACKET,
        ')': Tokens.RIGHT_ROUND_BRACKET,
        '[': Tokens.LEFT_BOX_BRACKET,
        ']': Tokens.RIGHT_BOX_BRACKET,
        '.': Tokens.DOT,
        ',': Tokens.COMMA,
        ';': Tokens.SEMI_COLON,
        '+': Tokens.PLUS,
        '-': Tokens.MINUS,
        '*': Tokens.MULTI,
        '/': Tokens.DIV,
        '&': Tokens.AND,
        '|': Tokens.PIPE,
        '<': Tokens.LESS_THAN,
        '>': Tokens.GREATER_THAN,
        '=': Tokens.EQUAL,
        '~': Tokens.TILDE
    }

    LINE_COMMENT_START = '//'

    COMMENT_START = '/*'

    COMMENT_END = '*/'

    IDENTIFIER_PATTERN = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

    INTEGER_PATTERN = re.compile(r'^[0-9]+$')

    STRING_PATTERN = re.compile(r'^".*"$')
