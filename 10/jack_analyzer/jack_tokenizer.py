from const import *
from token import *


token_convert = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;'
}


class JackTokenizer():
    def __init__(self, filepath):
        self.current_token = None
        self.linenum = 0
        self.remained_line = ''
        self.remained_tokens = []

        self.readfile = open(filepath)

        with open(filepath[:-5] + "T.myImpl.xml", 'w') as writef:
            writef.write('<tokens>\n')
            while 1:
                token = self.parse_next_token()
                if token:
                    elem_name = ''
                    if token.type == TokenType.SYMBOL:
                        elem_name = 'symbol'
                    elif token.type == TokenType.STRING_CONST:
                        elem_name = 'stringConstant'
                    elif token.type == TokenType.KEYWORD:
                        elem_name = 'keyword'
                    elif token.type == TokenType.IDENTIFIER:
                        elem_name = 'identifier'
                    elif token.type == TokenType.INT_CONST:
                        elem_name = 'integerConstant'

                    self.remained_tokens.append(token)

                    writef.write("<%s> %s </%s>\n" % (elem_name, token.token_escaped, elem_name))
                else:
                    break
            writef.write('</tokens>\n')
        self.readfile.close()

    def _readline(self):
        self.linenum += 1
        line = self.readfile.readline()
        if line:
            self.remained_line = line.split(Tokens.LINE_COMMENT_START.token)[0].strip()
            return self.remained_line
        else:
            self.remained_line = None
            return self.remained_line

    def parse_next_token(self):

        while True:
            # read new line
            if self.remained_line == '':

                self._readline()

                if self.remained_line is None:
                    return None

            if self.remained_line:
                return self._pop_token_from_remained_line()

    def _pop_token_from_remained_line(self):

        self.remained_line = self.remained_line.lstrip()

        for i in range(1, len(self.remained_line) + 1):

            t_0 = self.judge_token(self.remained_line[0:i])

            if t_0 == Tokens.COMMENT_START:
                while 1:
                    end_i = self.remained_line.find(Tokens.COMMENT_END.token)
                    if end_i > -1:
                        self.remained_line = self.remained_line[end_i + 2:]
                        if len(self.remained_line) > 0:
                            return self._pop_token_from_remained_line()
                        else:
                            self._readline()
                            return self._pop_token_from_remained_line()

                    self._readline()

            if i == len(self.remained_line):
                if self.judge_token(self.remained_line):
                    self.current_token = self.judge_token(self.remained_line[0:i])
                    self.remained_line = self.remained_line[i:]
                    return self.current_token
                else:
                    self.raise_exception('Unknown token exists')
            else:
                t_1 = self.judge_token(self.remained_line[0:i + 1])
                if t_0:
                    if t_1:
                        continue
                    else:
                        self.current_token = self.judge_token(self.remained_line[0:i])
                        self.remained_line = self.remained_line[i:]
                        return self.current_token

    def current_token_type(self):
        return self.judge_token(self.current_token)

    def raise_exception(self, msg):
        raise Exception('%s at line %d' % (msg, self.linenum))

    def advance(self):
        if len(self.remained_tokens) > 0:
            self.current_token = self.remained_tokens.pop(0)
        else:
            self.current_token = None
        return self.current_token

    def judge_token(self, judged_token):
        if judged_token in TOKEN_MAP:
            return TOKEN_MAP[judged_token]
        elif INTEGER_PATTERN.match(judged_token):
            try:
                return IntegerConstant(judged_token)
            except Exception as e:
                self.raise_exception(e.message)
        elif IDENTIFIER_PATTERN.match(judged_token):
            return Identifier(judged_token)
        elif STRING_PATTERN.match(judged_token):
            return StringConstant(judged_token[1:-1])
        else:
            return None

    def token_type(self):
        return self.current_token.type

    def close(self):
        self.readfile.close()

