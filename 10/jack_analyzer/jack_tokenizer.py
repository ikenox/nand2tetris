from constants import *

token_convert = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;'
}


class JackTokenizer():
    def __init__(self, filepath):
        self.current_token = None
        self.remained_line = ''
        self.linenum = 0
        self.readfile = open(filepath)
        self.tokens = []

        with open(filepath[:-5] + "T.myImpl.xml", 'w') as writef:
            writef.write('<tokens>\n')
            while 1:
                token = self.parse_next_token()
                if token:
                    tt = self.judge_token_type(token)

                    elem_name = ''
                    if tt == Constants.TokenType.SYMBOL:
                        elem_name = 'symbol'
                    elif tt == Constants.TokenType.STRING_CONST:
                        elem_name = 'stringConstant'
                        token = token[1:-1]
                    elif tt == Constants.TokenType.KEYWORD:
                        elem_name = 'keyword'
                    elif tt == Constants.TokenType.IDENTIFIER:
                        elem_name = 'identifier'
                    elif tt == Constants.TokenType.INT_CONST:
                        elem_name = 'integerConstant'

                    self.tokens.append(token)

                    if token in token_convert:
                        token = token_convert[token]

                    writef.write("<%s> %s </%s>\n" % (elem_name, token, elem_name))
                else:
                    break
            writef.write('</tokens>\n')

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.readfile.close()

    def _readline(self):
        self.linenum += 1
        line = self.readfile.readline()
        if line:
            self.remained_line = line.split(Constants.Tokens.LINE_COMMENT_START)[0].strip()
            return self.remained_line
        else:
            self.remained_line = None
            return self.remained_line

    def parse_next_token(self):

        while True:
            # read new line
            if self.remained_line == '':

                self._readline()

                if self.remained_line == None:
                    return None

            if self.remained_line:
                return self._pop_token_from_remained_line()

    def _pop_token_from_remained_line(self):

        self.remained_line = self.remained_line.lstrip()

        for i in range(1, len(self.remained_line) + 1):

            tt_0 = self.judge_token_type(self.remained_line[0:i])

            if tt_0 == Constants.TokenType.COMMENT_START:
                while 1:
                    end_i = self.remained_line.find(Constants.Tokens.COMMENT_END)
                    if end_i > -1:
                        self.remained_line = self.remained_line[end_i + 2:]
                        if len(self.remained_line) > 0:
                            return self._pop_token_from_remained_line()
                        else:
                            self._readline()
                            return self._pop_token_from_remained_line()

                    self._readline()

            if i == len(self.remained_line):
                if self.judge_token_type(self.remained_line):
                    self.current_token = self.remained_line[0:i]
                    self.remained_line = self.remained_line[i:]
                    return self.current_token
                else:
                    self.raise_exception('Unknown token exists')
            else:
                tt_1 = self.judge_token_type(self.remained_line[0:i + 1])
                if tt_0:
                    if tt_1:
                        continue
                    else:
                        self.current_token = self.remained_line[0:i]
                        self.remained_line = self.remained_line[i:]
                        return self.current_token

    def current_token_type(self):
        return self.judge_token_type(self.current_token)

    def raise_exception(self, msg):
        raise Exception('%s at line %d' % (msg, self.linenum))

    def advance(self):
        return self.tokens.pop(0)

    def judge_token_type(self, judged_token):
        if judged_token in Constants.Tokens.KEYWORDS:
            return Constants.TokenType.KEYWORD
        elif judged_token in Constants.Tokens.SYMBOLS:
            return Constants.TokenType.SYMBOL
        elif Constants.Tokens.INTEGER_PATTERN.match(judged_token):
            if int(judged_token) <= 32767:
                return Constants.TokenType.INT_CONST
            else:
                self.raise_exception('Too large integer')
        elif Constants.Tokens.IDENTIFIER_PATTERN.match(judged_token):
            return Constants.TokenType.IDENTIFIER
        elif Constants.Tokens.STRING_PATTERN.match(judged_token):
            return Constants.TokenType.STRING_CONST
        elif judged_token == Constants.Tokens.COMMENT_START:
            return Constants.TokenType.COMMENT_START
        else:
            return None
