from const import *
from jack_tokenizer import JackTokenizer
from symbol_table import SymbolTable


class CompilationEngine():
    def __init__(self, filepath, vm_writer):
        self.wf = open(filepath[:-5] + ".myImpl.xml", 'w')
        self.tokenizer = JackTokenizer(filepath)
        self.symbol_table = SymbolTable()
        self.vmw = vm_writer
        self.compiled_class_name = None
        self.label_num = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wf.close()

    def get_new_label(self):
        self.label_num += 1
        return 'LABEL_%d' % self.label_num

    def compile(self):
        self.compile_class()

    def compile_class(self):

        self.write_element_start('class')

        self.compile_keyword([Tokens.CLASS])
        self.compiled_class_name = self.compile_class_name().token
        self.compile_symbol(Tokens.LEFT_CURLY_BRACKET)

        while self.next_is_class_var_dec():
            self.compile_class_var_dec()

        while self.next_is_subroutine_dec():
            self.compile_subroutine_dec()

        self.compile_symbol(Tokens.RIGHT_CURLY_BRACKET)

        self.write_element_end('class')

    def compile_class_var_dec(self):
        self.write_element_start('classVarDec')

        token = self.compile_keyword([Tokens.STATIC, Tokens.FIELD])
        kind = None
        if token == Tokens.STATIC:
            kind = IdentifierKind.STATIC
        elif token == Tokens.FIELD:
            kind = IdentifierKind.FIELD
        else:
            self.raise_syntax_error('Unexpected token')

        type_token = self.compile_type()
        self.compile_var_name(declaration=True, type=type_token.token, kind=kind)

        while self.next_is(Tokens.COMMA):
            self.compile_symbol(Tokens.COMMA)
            self.compile_var_name(declaration=True, type=type_token.token, kind=kind)

        self.compile_symbol(Tokens.SEMI_COLON)

        self.write_element_end('classVarDec')

    def compile_var_dec(self):

        self.write_element_start('varDec')
        self.compile_keyword(Tokens.VAR)
        type_token = self.compile_type()
        var_num = 0
        self.compile_var_name(declaration=True, type=type_token.token, kind=IdentifierKind.VAR)
        var_num += 1
        while self.next_is(Tokens.COMMA):
            self.compile_symbol(Tokens.COMMA)
            self.compile_var_name(declaration=True, type=type_token.token, kind=IdentifierKind.VAR)
            var_num += 1
        self.compile_symbol(Tokens.SEMI_COLON)
        self.write_element_end('varDec')

        return var_num

    def compile_subroutine_dec(self):
        self.symbol_table.start_subroutine()

        self.write_element_start('subroutineDec')

        token = self.compile_keyword([Tokens.CONSTRUCTOR, Tokens.FUNCTION, Tokens.METHOD])
        if self.tokenizer.see_next() == Tokens.VOID:
            self.compile_keyword(Tokens.VOID)
        else:
            self.compile_type()
        subroutine_name = self.compile_subroutine_name().token
        self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)

        if token == Tokens.METHOD:
            self.symbol_table.define('$this',self.compiled_class_name,IdentifierKind.ARG)

        self.compile_parameter_list()
        self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
        self.compile_subroutine_body(subroutine_name, token)

        self.write_element_end('subroutineDec')

    def compile_subroutine_name(self):
        self.write_identifier_info('category: subroutine')
        return self.compile_identifier()

    def compile_class_name(self):
        self.write_identifier_info('category: class')
        return self.compile_identifier()

    def compile_var_name(self, declaration=False, type=None, kind=None, let=False):
        if declaration:
            self.symbol_table.define(self.tokenizer.see_next().token, type, kind)
        elif let:
            pass
        else:
            kind = self.symbol_table.kind_of(self.tokenizer.see_next().token)
            if kind == IdentifierKind.ARG:
                self.vmw.write_push(Segment.ARG, self.symbol_table.index_of(self.tokenizer.see_next().token))
            elif kind == IdentifierKind.VAR:
                self.vmw.write_push(Segment.LOCAL, self.symbol_table.index_of(self.tokenizer.see_next().token))
            elif kind == IdentifierKind.FIELD:
                self.vmw.write_push(Segment.THIS, self.symbol_table.index_of(self.tokenizer.see_next().token))
            elif kind == IdentifierKind.STATIC:
                self.vmw.write_push(Segment.STATIC, self.symbol_table.index_of(self.tokenizer.see_next().token))

        self.write_identifier_info('declaration: %s, kind: %s, index: %d' % (
            declaration, self.symbol_table.kind_of(self.tokenizer.see_next().token),
            self.symbol_table.index_of(self.tokenizer.see_next().token)))
        return self.compile_identifier()

    def write_identifier_info(self, value):
        self.write_element('IdentifierInfo', value)

    def compile_parameter_list(self):
        self.write_element_start('parameterList')

        if self.tokenizer.see_next() in [Tokens.INT, Tokens.CHAR, Tokens.BOOLEAN] or isinstance(
                self.tokenizer.see_next(), Identifier):
            type_token = self.compile_type()
            self.compile_var_name(declaration=True, type=type_token.token, kind=IdentifierKind.ARG)

            while self.next_is(Tokens.COMMA):
                self.compile_symbol(Tokens.COMMA)
                type_token = self.compile_type()
                self.compile_var_name(declaration=True, type=type_token.token, kind=IdentifierKind.ARG)

        self.write_element_end('parameterList')

    def compile_subroutine_body(self, subroutine_name, subroutine_dec_token):
        self.write_element_start('subroutineBody')

        print subroutine_name,subroutine_dec_token

        self.compile_symbol(Tokens.LEFT_CURLY_BRACKET)
        local_num = 0
        while self.next_is(Tokens.VAR):
            var_num = self.compile_var_dec()
            local_num += var_num

        self.vmw.write_function("%s.%s" % (self.compiled_class_name, subroutine_name), local_num)

        if subroutine_dec_token == Tokens.METHOD:
            self.vmw.write_push(Segment.ARG, 0)
            self.vmw.write_pop(Segment.POINTER, 0)
        elif subroutine_dec_token == Tokens.CONSTRUCTOR:
            self.vmw.write_push(Segment.CONST, self.symbol_table.var_count(IdentifierKind.FIELD))
            self.vmw.write_call('Memory.alloc', 1)
            self.vmw.write_pop(Segment.POINTER, 0)
        elif subroutine_dec_token == Tokens.FUNCTION:
            pass
        else:
            self.raise_syntax_error('Invalid token')

        self.compile_statements()
        self.compile_symbol(Tokens.RIGHT_CURLY_BRACKET)

        self.write_element_end('subroutineBody')

        print "========="
        for key in self.symbol_table.arg_table:
            print self.symbol_table.arg_table[key].type,key,"kind:",self.symbol_table.arg_table[key].kind,"index:",self.symbol_table.arg_table[key].index

        return local_num

    def compile_statements(self):
        self.write_element_start('statements')

        while self.next_is_statement():
            self.compile_statement()

        self.write_element_end('statements')

    def compile_statement(self):
        if self.next_is(Tokens.LET):
            self.write_element_start('letStatement')
            self.compile_keyword(Tokens.LET)
            let_var = self.compile_var_name(let=True).token

            if self.next_is(Tokens.LEFT_BOX_BRACKET):
                self.compile_symbol(Tokens.LEFT_BOX_BRACKET)
                self.compile_expression()  # i
                self.compile_symbol(Tokens.RIGHT_BOX_BRACKET)
                self.compile_symbol(Tokens.EQUAL)

                # base address
                kind = self.symbol_table.kind_of(let_var)
                if kind == IdentifierKind.ARG:
                    self.vmw.write_push(Segment.ARG, self.symbol_table.index_of(let_var))
                elif kind == IdentifierKind.VAR:
                    self.vmw.write_push(Segment.LOCAL, self.symbol_table.index_of(let_var))
                elif kind == IdentifierKind.FIELD:
                    self.vmw.write_push(Segment.THIS, self.symbol_table.index_of(let_var))
                elif kind == IdentifierKind.STATIC:
                    self.vmw.write_push(Segment.STATIC, self.symbol_table.index_of(let_var))

                # temp_2 <- base + i
                self.vmw.write_arithmetic(Command.ADD)
                self.vmw.write_pop(Segment.TEMP, 2)

                # value
                self.compile_expression()

                # set THAT <- base+i
                self.vmw.write_push(Segment.TEMP, 2)
                self.vmw.write_pop(Segment.POINTER, 1)

                self.vmw.write_pop(Segment.THAT, 0)
                self.compile_symbol(Tokens.SEMI_COLON)

            else:
                self.compile_symbol(Tokens.EQUAL)
                self.compile_expression()
                self.compile_symbol(Tokens.SEMI_COLON)
                kind = self.symbol_table.kind_of(let_var)
                if kind == IdentifierKind.VAR:
                    self.vmw.write_pop(Segment.LOCAL, self.symbol_table.index_of(let_var))
                elif kind == IdentifierKind.ARG:
                    self.vmw.write_pop(Segment.ARG, self.symbol_table.index_of(let_var))
                elif kind == IdentifierKind.FIELD:
                    self.vmw.write_pop(Segment.THIS, self.symbol_table.index_of(let_var))
                elif kind == IdentifierKind.STATIC:
                    self.vmw.write_pop(Segment.STATIC, self.symbol_table.index_of(let_var))

            self.write_element_end('letStatement')

        elif self.next_is(Tokens.IF):
            self.write_element_start('ifStatement')
            self.compile_keyword(Tokens.IF)
            self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
            self.compile_expression()
            self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
            self.vmw.write_arithmetic(Command.NOT)
            l1 = self.get_new_label()
            l2 = self.get_new_label()
            self.vmw.write_if(l1)
            self.compile_symbol(Tokens.LEFT_CURLY_BRACKET)
            self.compile_statements()
            self.compile_symbol(Tokens.RIGHT_CURLY_BRACKET)
            self.vmw.write_goto(l2)
            self.vmw.write_label(l1)
            if self.next_is(Tokens.ELSE):
                self.compile_keyword(Tokens.ELSE)
                self.compile_symbol(Tokens.LEFT_CURLY_BRACKET)
                self.compile_statements()
                self.compile_symbol(Tokens.RIGHT_CURLY_BRACKET)
            self.vmw.write_label(l2)
            self.write_element_end('ifStatement')

        elif self.next_is(Tokens.WHILE):
            self.write_element_start('whileStatement')
            l1 = self.get_new_label()
            l2 = self.get_new_label()
            self.compile_keyword(Tokens.WHILE)
            self.vmw.write_label(l1)
            self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
            self.compile_expression()
            self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
            self.vmw.write_arithmetic(Command.NOT)
            self.vmw.write_if(l2)
            self.compile_symbol(Tokens.LEFT_CURLY_BRACKET)
            self.compile_statements()
            self.compile_symbol(Tokens.RIGHT_CURLY_BRACKET)
            self.vmw.write_goto(l1)
            self.vmw.write_label(l2)
            self.write_element_end('whileStatement')

        elif self.next_is(Tokens.DO):
            self.write_element_start('doStatement')
            self.compile_keyword(Tokens.DO)
            self.compile_subroutine_call()
            self.compile_symbol(Tokens.SEMI_COLON)
            self.write_element_end('doStatement')
            self.vmw.write_pop(Segment.TEMP, 0)

        elif self.next_is(Tokens.RETURN):
            self.write_element_start('returnStatement')
            self.compile_keyword(Tokens.RETURN)
            if not self.next_is(Tokens.SEMI_COLON):
                self.compile_expression()
            else:
                self.vmw.write_push(Segment.CONST, 0)

            self.compile_symbol(Tokens.SEMI_COLON)
            self.vmw.write_return()

            self.write_element_end('returnStatement')

    def compile_subroutine_call(self):
        if self.next_is(Tokens.LEFT_ROUND_BRACKET, idx=1):
            subroutinename = self.compile_subroutine_name().token
            self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
            self.vmw.write_push(Segment.POINTER, 0)
            argnum = self.compile_expression_list()
            self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
            self.vmw.write_call("%s.%s" % (self.compiled_class_name, subroutinename), argnum + 1)
        else:
            identifier_str = self.tokenizer.see_next().token
            if self.symbol_table.kind_of(identifier_str):
                instance_name = self.compile_var_name().token
                self.compile_symbol(Tokens.DOT)
                subroutinename = self.compile_subroutine_name().token
                self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
                kind = self.symbol_table.kind_of(instance_name)
                if kind == IdentifierKind.ARG:
                    self.vmw.write_push(Segment.ARG, self.symbol_table.index_of(instance_name))
                elif kind == IdentifierKind.VAR:
                    self.vmw.write_push(Segment.LOCAL, self.symbol_table.index_of(instance_name))
                elif kind == IdentifierKind.FIELD:
                    self.vmw.write_push(Segment.THIS, self.symbol_table.index_of(instance_name))
                elif kind == IdentifierKind.STATIC:
                    self.vmw.write_push(Segment.STATIC, self.symbol_table.index_of(instance_name))
                argnum = self.compile_expression_list()
                self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
                self.vmw.write_call("%s.%s" % (self.symbol_table.type_of(instance_name), subroutinename), argnum + 1)
            else:
                classname = self.compile_class_name().token
                self.compile_symbol(Tokens.DOT)
                subroutinename = self.compile_subroutine_name().token
                self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
                argnum = self.compile_expression_list()
                self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
                self.vmw.write_call("%s.%s" % (classname, subroutinename), argnum)

    def compile_expression_list(self):
        self.write_element_start('expressionList')
        argnum = 0
        if not self.next_is(Tokens.RIGHT_ROUND_BRACKET):
            self.compile_expression()
            argnum += 1
            while self.next_is(Tokens.COMMA):
                self.compile_symbol(Tokens.COMMA)
                self.compile_expression()
                argnum += 1
        self.write_element_end('expressionList')

        return argnum

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
            op_token = self.compile_symbol([
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
            if op_token == Tokens.PLUS:
                self.vmw.write_arithmetic(Command.ADD)
            elif op_token == Tokens.MINUS:
                self.vmw.write_arithmetic(Command.SUB)
            elif op_token == Tokens.MULTI:
                self.vmw.write_call('Math.multiply', 2)
            elif op_token == Tokens.DIV:
                self.vmw.write_call('Math.divide', 2)
            elif op_token == Tokens.AND:
                self.vmw.write_arithmetic(Command.AND)
            elif op_token == Tokens.PIPE:
                self.vmw.write_arithmetic(Command.OR)
            elif op_token == Tokens.LESS_THAN:
                self.vmw.write_arithmetic(Command.LT)
            elif op_token == Tokens.GREATER_THAN:
                self.vmw.write_arithmetic(Command.GT)
            elif op_token == Tokens.EQUAL:
                self.vmw.write_arithmetic(Command.EQ)

        self.write_element_end('expression')

    def compile_term(self):
        self.write_element_start('term')

        if self.next_type_is(TokenType.INT_CONST):
            value_str = self.compile_integer_constant()
            self.vmw.write_push(Segment.CONST, value_str)
        elif self.next_type_is(TokenType.STRING_CONST):
            self.compile_string_constant()
        elif self.next_is(Tokens.NULL):
            self.compile_keyword(Tokens.NULL)
            self.vmw.write_push(Segment.CONST, 0)
        elif self.next_is(Tokens.THIS):
            self.compile_keyword(Tokens.THIS)
            self.vmw.write_push(Segment.POINTER, 0)
        elif self.next_is(Tokens.TRUE):
            self.compile_keyword(Tokens.TRUE)
            self.vmw.write_push(Segment.CONST, 0)
            self.vmw.write_arithmetic(Command.NOT)
        elif self.next_is(Tokens.FALSE):
            self.compile_keyword(Tokens.FALSE)
            self.vmw.write_push(Segment.CONST, 0)
        elif self.next_type_is(TokenType.IDENTIFIER):
            if self.next_is(Tokens.LEFT_BOX_BRACKET, idx=1):

                var_name = self.compile_var_name().token
                self.compile_symbol(Tokens.LEFT_BOX_BRACKET)
                self.compile_expression()

                self.vmw.write_arithmetic(Command.ADD)
                self.vmw.write_pop(Segment.POINTER, 1)
                self.vmw.write_push(Segment.THAT, 0)
                self.compile_symbol(Tokens.RIGHT_BOX_BRACKET)
            elif self.next_is([Tokens.LEFT_ROUND_BRACKET, Tokens.DOT], idx=1):
                self.compile_subroutine_call()
            else:
                self.compile_var_name()

        elif self.next_is(Tokens.LEFT_ROUND_BRACKET):
            self.compile_symbol(Tokens.LEFT_ROUND_BRACKET)
            self.compile_expression()
            self.compile_symbol(Tokens.RIGHT_ROUND_BRACKET)
        elif self.next_is(Tokens.TILDE):
            self.compile_symbol(Tokens.TILDE)
            self.compile_term()
            self.vmw.write_arithmetic(Command.NOT)
        elif self.next_is(Tokens.MINUS):
            self.compile_symbol(Tokens.MINUS)
            self.compile_term()
            self.vmw.write_arithmetic(Command.NEG)
        else:
            self.raise_syntax_error('')
        self.write_element_end('term')

    def next_type_is(self, token_type):
        return self.tokenizer.see_next().type == token_type

    def compile_type(self):
        type_token = self.tokenizer.see_next()

        if self.next_is([Tokens.INT, Tokens.CHAR, Tokens.BOOLEAN]):
            self.compile_keyword([Tokens.INT, Tokens.CHAR, Tokens.BOOLEAN])
        else:
            self.compile_class_name()
        return type_token

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
                return self.tokenizer.current_token
            else:
                self.raise_syntax_error('')
        else:
            if self.tokenizer.current_token == tokens:
                self.write_element('symbol', self.tokenizer.current_token.token_escaped)
                return self.tokenizer.current_token
            else:
                self.raise_syntax_error('')

    def compile_keyword(self, tokens):
        self.tokenizer.advance()
        if type(tokens) == list:
            if self.tokenizer.current_token in tokens:
                self.write_element('keyword', self.tokenizer.current_token.token_escaped)
                return self.tokenizer.current_token
            else:
                self.raise_syntax_error('')
        else:
            if self.tokenizer.current_token == tokens:
                self.write_element('keyword', self.tokenizer.current_token.token_escaped)
                return self.tokenizer.current_token
            else:
                self.raise_syntax_error('')

    def compile_identifier(self):
        self.tokenizer.advance()
        if isinstance(self.tokenizer.current_token, Identifier):
            identifier_str = self.tokenizer.current_token.token_escaped
            self.write_element(
                'identifier',
                identifier_str
            )
            return self.tokenizer.current_token
        else:
            self.raise_syntax_error('')

    def compile_integer_constant(self):
        self.tokenizer.advance()
        if isinstance(self.tokenizer.current_token, IntegerConstant):
            self.write_element('integerConstant', self.tokenizer.current_token.token_escaped)
            return self.tokenizer.current_token.token_escaped
        else:
            self.raise_syntax_error('')

    def compile_string_constant(self):
        self.tokenizer.advance()
        if isinstance(self.tokenizer.current_token, StringConstant):
            string = self.tokenizer.current_token.token
            self.write_element('stringConstant', self.tokenizer.current_token.token_escaped)
            self.vmw.write_push(Segment.CONST, len(string))
            self.vmw.write_call('String.new', 1)
            for c in string:
                self.vmw.write_push(Segment.CONST, ord(c))
                self.vmw.write_call('String.appendChar', 2)
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
