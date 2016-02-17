from const import *
from jack_tokenizer import JackTokenizer


class CompilationEngine():
    def __init__(self, filepath):
        self.wf = open(filepath[:-5] + ".myImpl.xml", 'w')
        self.tokenizer = JackTokenizer(filepath)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wf.close()

    def compile(self):
        self.compile_class()

    def compile_class(self):
        self.write_element_start('class')

        self.compile_keyword(Tokens.CLASS)
        self.compile_identifier()
        self.compile_symbol(Tokens.LEFT_CURLY_BRACKET)

        while self.next_is_class_var_dec():
            self.compile_class_var_dec()

        while self.next_is_subroutine_dec():
            self.compile_subroutine_dec()

        self.compile_symbol(Tokens.RIGHT_CURLY_BRACKET)

        self.write_element_end('class')

    def next_is_class_var_dec(self):
        return self.tokenizer.see_next() == Tokens.STATIC or self.tokenizer.see_next() == Tokens.FIELD

    def next_is_subroutine_dec(self):
        return self.tokenizer.see_next() == Tokens.CONSTRUCTOR or self.tokenizer.see_next() == Tokens.FUNCTION or self.tokenizer.see_next() == Tokens.METHOD

    def compile_symbol(self, token):
        self.tokenizer.advance()
        if self.tokenizer.current_token == token:
            self.write_element('symbol', self.tokenizer.current_token.token_escaped)
        else:
            self.raise_syntax_error('c')

    def compile_keyword(self, token):
        self.tokenizer.advance()
        if self.tokenizer.current_token == token:
            self.write_element('keyword', self.tokenizer.current_token.token_escaped)
        else:
            self.raise_syntax_error('')

    def compile_identifier(self):
        self.tokenizer.advance()
        if isinstance(self.tokenizer.current_token, Identifier):
            self.write_element('identifier', self.tokenizer.current_token.token_escaped)
        else:
            self.raise_syntax_error('')

    def compile_integer_constant(self):
        self.tokenizer.advance()
        if isinstance(self.tokenizer.current_token, IntegerConstant):
            self.write_element('integerConstant', self.tokenizer.current_token.token_escaped)
        else:
            self.raise_syntax_error('')

    def compile_string_constant(self):
        self.tokenizer.advance()
        if isinstance(self.tokenizer.current_token, IntegerConstant):
            self.write_element('stringConstant', self.tokenizer.current_token.token_escaped)
        else:
            self.raise_syntax_error('')

    def write_element(self, elem_name, value):
        self.wf.write('<%s> %s </%s>\n' % (elem_name, value, elem_name))

    def write_element_start(self, elem_name):
        self.wf.write('<%s>\n' % elem_name)

    def write_element_end(self, elem_name):
        self.wf.write('</%s>\n' % elem_name)

    def raise_syntax_error(self, msg):
        raise Exception('%s' % msg)
