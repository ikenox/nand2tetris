from constants import *
from jack_tokenizer import JackTokenizer

class CompilationEngine():

    def __enter__(self,filepath):
        self.wf = open(filepath[:-5] + ".myImpl.xml", 'w')
        self.tokenizer = JackTokenizer(filepath)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wf.close()

    def compile(self):
        self.compile_class()

    def compile_class(self):
        self.tokenizer.advance()
        if Constants.Tokens.KEYWORDS[self.tokenizer.current_token] == KeyWords.CLASS:
            self.write_element('keyword', self.tokenizer.keyword())

            self.tokenizer.advance()
            if self.tokenizer.token_type() == Constants.TokenType.IDENTIFIER:
                self.write_element('', self.tokenizer.identifier())

        raise self.raise_syntax_error('syntax error')



    def write_element(self, elem_name, value):
        self.wf.write('<%s> %s </%s>\n' % (elem_name, value, elem_name))

    def raise_syntax_error(self,msg):
        raise Exception('%s')