from const import *
from jack_tokenizer import JackTokenizer

class CompilationEngine():

    def __init__(self,filepath):
        self.wf = open(filepath[:-5] + ".myImpl.xml", 'w')
        self.tokenizer = JackTokenizer(filepath)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wf.close()

    def compile(self):
        self.wf.write('<class>')
        # self.compile_class()
        self.wf.write('</class>')

    # def compile_class(self):
    #
    #     self.tokenizer.advance()
    #     if Constants.Tokens.KEYWORDS[self.tokenizer.current_token] == KeyWords.CLASS:
    #         self.write_element('keyword', self.tokenizer.keyword())
    #
    #         self.compile_class_name()
    #
    #         self.tokenizer.advance()
    #         if self.tokenizer.symbol() == '{':
    #             self.write_element('symbol', self.tokenizer.symbol())
    #
    #     raise self.raise_syntax_error('syntax error')
    #
    # def compile_class_name(self):
    #     self.tokenizer.advance()
    #     if self.tokenizer.token_type() == Constants.TokenType.IDENTIFIER:
    #         self.write_element('identifier', self.tokenizer.identifier())
    #         return

        raise self.raise_syntax_error('syntax error')

    def write_element(self, elem_name, value):
        self.wf.write('<%s> %s </%s>\n' % (elem_name, value, elem_name))

    def raise_syntax_error(self,msg):
        raise Exception('%s' % msg)