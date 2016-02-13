import re


class Constants:
    class Tokens:
        KEYWORDS = [
            'class',
            'constructor',
            'function',
            'method',
            'field',
            'static',
            'var',
            'int',
            'char',
            'boolean',
            'void',
            'true',
            'false',
            'this',
            'let',
            'do',
            'if',
            'else',
            'while',
            'return'
        ]

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
