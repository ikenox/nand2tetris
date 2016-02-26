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

        self.compile_keyword([Tokens.CLASS])
        self.compile_class_name()
        self.compile_symbol(Tokens.LEFT_CURLY_BRACKET)

        while self.next_is_class_var_dec():
            self.compile_class_var_dec()

        while self.next_is_subroutine_dec():
            self.compile_subroutine_dec()

        self.compile_symbol(Tokens.RIGHT_CURLY_BRACKET)

        self.write_element_end('class')

    def compile_class_var_dec(self):
        self.write_element_start('classVarDec')

        self.compile_keyword([Tokens.STATIC, Tokens.FIELD])
        self.compile_type()
        self.compile_var_name()

        while self.next_is(Tokens.COMMA):
            self.compile_symbol(Tokens.COMMA)
            self.compile_var_name()

        self.compile_symbol(Tokens.SEMI_COLON)

        self.write_element_end('classVarDec')

    def compile_subroutine_dec(self):
        self.write_element_start('subroutineDec')

        self.compile_keyword([Tokens.CONSTRUCTOR, Tokens.FUNCTION, Tokens.METHOD])
        if self.tokenizer.see_next() == Tokens.VOID:
            self.compile_keyword(Tokens.VOID)
        else:
            self.compile_type()
        self.compile_subroutine_name()
        self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
        self.compile_parameter_list()
        self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
        self.compile_subroutine_body()

        self.write_element_end('subroutineDec')

    def compile_subroutine_name(self):
        self.compile_identifier()

    def compile_class_name(self):
        self.compile_identifier()

    def compile_var_name(self):
        self.compile_identifier()

    def compile_parameter_list(self):
        self.write_element_start('parameterList')

        if self.tokenizer.see_next() in [Tokens.INT, Tokens.CHAR, Tokens.BOOLEAN] or isinstance(
                self.tokenizer.see_next(), Identifier):
            self.compile_type()
            self.compile_var_name()

            while self.next_is(Tokens.COMMA):
                self.compile_symbol(Tokens.COMMA)
                self.compile_type()
                self.compile_var_name()

        self.write_element_end('parameterList')

    def compile_subroutine_body(self):
        self.write_element_start('subroutineBody')

        self.compile_symbol(Tokens.LEFT_CURLY_BRACKET)
        while self.next_is(Tokens.VAR):
            self.compile_var_dec()

        self.compile_statements()
        self.compile_symbol(Tokens.RIGHT_CURLY_BRACKET)

        self.write_element_end('subroutineBody')

    def compile_var_dec(self):
        self.write_element_start('varDec')
        self.compile_keyword(Tokens.VAR)
        self.compile_type()
        self.compile_var_name()
        while self.next_is(Tokens.COMMA):
            self.compile_symbol(Tokens.COMMA)
            self.compile_var_name()
        self.compile_symbol(Tokens.SEMI_COLON)
        self.write_element_end('varDec')

    def compile_statements(self):
        self.write_element_start('statements')

        while self.next_is_statement():
            self.compile_statement()

        self.write_element_end('statements')

    def compile_statement(self):
        if self.next_is(Tokens.LET):
            self.write_element_start('letStatement')
            self.compile_keyword(Tokens.LET)
            self.compile_var_name()
            if self.next_is(Tokens.LEFT_BOX_BRACKET):
                self.compile_symbol(Tokens.LEFT_BOX_BRACKET)
                self.compile_expression()
                self.compile_symbol(Tokens.RIGHT_BOX_BRACKET)
            self.compile_symbol(Tokens.EQUAL)
            self.compile_expression()
            self.compile_symbol(Tokens.SEMI_COLON)
            self.write_element_end('letStatement')

        elif self.next_is(Tokens.IF):
            self.write_element_start('ifStatement')
            self.compile_keyword(Tokens.IF)
            self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
            self.compile_expression()
            self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
            self.compile_symbol(Tokens.LEFT_CURLY_BRACKET)
            self.compile_statements()
            self.compile_symbol(Tokens.RIGHT_CURLY_BRACKET)
            if self.next_is(Tokens.ELSE):
                self.compile_keyword(Tokens.ELSE)
                self.compile_symbol(Tokens.LEFT_CURLY_BRACKET)
                self.compile_statements()
                self.compile_symbol(Tokens.RIGHT_CURLY_BRACKET)
            self.write_element_end('ifStatement')

        elif self.next_is(Tokens.WHILE):
            self.write_element_start('whileStatement')
            self.compile_keyword(Tokens.WHILE)
            self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
            self.compile_expression()
            self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
            self.compile_symbol(Tokens.LEFT_CURLY_BRACKET)
            self.compile_statements()
            self.compile_symbol(Tokens.RIGHT_CURLY_BRACKET)
            self.write_element_end('whileStatement')

        elif self.next_is(Tokens.DO):
            self.write_element_start('doStatement')
            self.compile_keyword(Tokens.DO)
            self.compile_subroutine_call()
            self.compile_symbol(Tokens.SEMI_COLON)
            self.write_element_end('doStatement')

        elif self.next_is(Tokens.RETURN):
            self.write_element_start('returnStatement')
            self.compile_keyword(Tokens.RETURN)
            if not self.next_is(Tokens.SEMI_COLON):
                self.compile_expression()
            self.compile_symbol(Tokens.SEMI_COLON)

            self.write_element_end('returnStatement')

    def compile_subroutine_call(self):
        if self.next_is(Tokens.LEFT_ROUND_BRACKET, idx=1):
            self.compile_subroutine_name()
            self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
            self.compile_expression_list()
            self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
        else:
            self.compile_identifier()
            self.compile_symbol(Tokens.DOT)
            self.compile_subroutine_name()
            self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
            self.compile_expression_list()
            self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)

    def compile_expression_list(self):
        self.write_element_start('expressionList')
        if not self.next_is(Tokens.RIGHT_ROUND_BRACKET):
            self.compile_expression()
            while self.next_is(Tokens.COMMA):
                self.compile_symbol(Tokens.COMMA)
                self.compile_expression()
        self.write_element_end('expressionList')

    def compile_expression(self):
        self.write_element_start('expression')
        self.compile_term()
        while self.next_is([
            Tokens.PLUS,
            Tokens.MINUS,
            Tokens.MULTI,
            Tokens.DIV,
            Tokens.AND,
            Tokens.PIPE,
            Tokens.LESS_THAN,
            Tokens.GREATER_THAN,
            Tokens.EQUAL]):
            self.compile_symbol([
                Tokens.PLUS,
                Tokens.MINUS,
                Tokens.MULTI,
                Tokens.DIV,
                Tokens.AND,
                Tokens.PIPE,
                Tokens.LESS_THAN,
                Tokens.GREATER_THAN,
                Tokens.EQUAL])
            self.compile_term()
        self.write_element_end('expression')

    def compile_term(self):
        self.write_element_start('term')

        if self.next_type_is(TokenType.INT_CONST):
            self.compile_integer_constant()
        elif self.next_type_is(TokenType.STRING_CONST):
            self.compile_string_constant()
        elif self.next_is([Tokens.NULL, Tokens.THIS, Tokens.TRUE, Tokens.FALSE]):
            self.compile_keyword([Tokens.NULL, Tokens.THIS, Tokens.TRUE, Tokens.FALSE])
        elif self.next_type_is(TokenType.IDENTIFIER):

            if self.next_is(Tokens.LEFT_BOX_BRACKET, idx=1):
                self.compile_var_name()
                self.compile_symbol(Tokens.LEFT_BOX_BRACKET)
                self.compile_expression()
                self.compile_symbol(Tokens.RIGHT_BOX_BRACKET)
            elif self.next_is([Tokens.LEFT_ROUND_BRACKET, Tokens.DOT], idx=1):
                self.compile_subroutine_call()
            else:
                self.compile_var_name()

        elif self.next_is(Tokens.LEFT_ROUND_BRACKET):
            self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
            self.compile_expression()
            self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
        elif self.next_is([Tokens.TILDE, Tokens.MINUS]):
            self.compile_symbol([Tokens.TILDE, Tokens.MINUS])
            self.compile_term()
        else:
            self.raise_syntax_error('')
        self.write_element_end('term')

    def next_type_is(self, token_type):
        return self.tokenizer.see_next().type == token_type

    def compile_type(self):
        if self.next_is([Tokens.INT, Tokens.CHAR, Tokens.BOOLEAN]):
            self.compile_keyword([Tokens.INT, Tokens.CHAR, Tokens.BOOLEAN])
        elif isinstance(self.tokenizer.see_next(), Identifier):
            self.compile_identifier()

    def next_is_statement(self):
        return self.next_is([Tokens.LET, Tokens.IF, Tokens.WHILE, Tokens.DO, Tokens.RETURN])

    def next_is(self, tokens, idx=0):
        if type(tokens) == list:
            return self.tokenizer.see_next(idx=idx) in tokens
        else:
            return self.tokenizer.see_next(idx=idx) == tokens

    def next_is_class_var_dec(self):
        return self.next_is([Tokens.STATIC, Tokens.FIELD])

    def next_is_subroutine_dec(self):
        return self.next_is([Tokens.CONSTRUCTOR, Tokens.FUNCTION, Tokens.METHOD])

    def compile_symbol(self, tokens):
        self.tokenizer.advance()
        if type(tokens) == list:
            if self.tokenizer.current_token in tokens:
                self.write_element('symbol', self.tokenizer.current_token.token_escaped)
            else:
                self.raise_syntax_error('')
        else:
            if self.tokenizer.current_token == tokens:
                self.write_element('symbol', self.tokenizer.current_token.token_escaped)
            else:
                self.raise_syntax_error('')

    def compile_keyword(self, tokens):
        self.tokenizer.advance()
        if type(tokens) == list:
            if self.tokenizer.current_token in tokens:
                self.write_element('keyword', self.tokenizer.current_token.token_escaped)
            else:
                self.raise_syntax_error('')
        else:
            if self.tokenizer.current_token == tokens:
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
        if isinstance(self.tokenizer.current_token, StringConstant):
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
