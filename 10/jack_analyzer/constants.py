import re


class KeyWords:
    CLASS = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    INT = 5
    BOOLEAN = 6
    CHAR = 7
    VOID = 8
    VAR = 9
    STATIC = 10
    FIELD = 11
    LET = 12
    DO = 13
    IF = 14
    ELSE = 15
    WHILE = 16
    RETURN = 17
    TRUE = 18
    FALSE = 19
    NULL = 20
    THIS = 21


class Constants:

    class TokenType:
        SYMBOL = 1
        IDENTIFIER = 2
        INT_CONST = 3
        STRING_CONST = 4
        KEYWORD = 5
        COMMENT_START = 6
        COMMENT_END = 6

    class Tokens:
        KEYWORDS = {
            'class': KeyWords.CLASS,
            'constructor': KeyWords.CONSTRUCTOR,
            'function': KeyWords.FUNCTION,
            'method': KeyWords.METHOD,
            'field': KeyWords.FIELD,
            'static': KeyWords.STATIC,
            'var': KeyWords.VAR,
            'int': KeyWords.INT,
            'char': KeyWords.CHAR,
            'boolean': KeyWords.BOOLEAN,
            'void': KeyWords.VOID,
            'true': KeyWords.TRUE,
            'false': KeyWords.FALSE,
            'null': KeyWords.NULL,
            'this': KeyWords.THIS,
            'let': KeyWords.LET,
            'do': KeyWords.DO,
            'if': KeyWords.IF,
            'else': KeyWords.ELSE,
            'while': KeyWords.WHILE,
            'return': KeyWords.RETURN
        }

        SYMBOLS = [
            '{',
            '}',
            '(',
            ')',
            '[',
            ']',
            '.',
            ',',
            ';',
            '+',
            '-',
            '*',
            '/',
            '&',
            '|',
            '<',
            '>',
            '=',
            '~'
        ]

        LINE_COMMENT_START = '//'

        COMMENT_START = '/*'

        COMMENT_END = '*/'

        IDENTIFIER_PATTERN = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

        INTEGER_PATTERN = re.compile(r'^[0-9]+$')

        STRING_PATTERN = re.compile(r'^".*"$')

class TokenType:
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4
    KEYWORD = 5
    COMMENT_START = 6
    COMMENT_END = 6

class Tokens:
    KEYWORDS = {
        'class': KeyWords.CLASS,
        'constructor': KeyWords.CONSTRUCTOR,
        'function': KeyWords.FUNCTION,
        'method': KeyWords.METHOD,
        'field': KeyWords.FIELD,
        'static': KeyWords.STATIC,
        'var': KeyWords.VAR,
        'int': KeyWords.INT,
        'char': KeyWords.CHAR,
        'boolean': KeyWords.BOOLEAN,
        'void': KeyWords.VOID,
        'true': KeyWords.TRUE,
        'false': KeyWords.FALSE,
        'null': KeyWords.NULL,
        'this': KeyWords.THIS,
        'let': KeyWords.LET,
        'do': KeyWords.DO,
        'if': KeyWords.IF,
        'else': KeyWords.ELSE,
        'while': KeyWords.WHILE,
        'return': KeyWords.RETURN
    }

    SYMBOLS = [
        '{',
        '}',
        '(',
        ')',
        '[',
        ']',
        '.',
        ',',
        ';',
        '+',
        '-',
        '*',
        '/',
        '&',
        '|',
        '<',
        '>',
        '=',
        '~'
    ]

    LINE_COMMENT_START = '//'

    COMMENT_START = '/*'

    COMMENT_END = '*/'

    IDENTIFIER_PATTERN = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

    INTEGER_PATTERN = re.compile(r'^[0-9]+$')

    STRING_PATTERN = re.compile(r'^".*"$')
