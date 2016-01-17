from constants import *

class CodeWriter():
    def __init__(self, filepath):
        self.f = open(filepath, 'w')
        self.label_num = 0

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.f.close()

    def set_file_name(self, file_name):
        pass

    def write_arithmetic(self, command):
        if command == "add":
            self.write_pop_to_m_register()
            self.write_code('D=M')
            self.write_pop_to_m_register()
            self.write_code('D=D+M')
            self.write_push_from_d_register()
        elif command == "sub":
            self.write_pop_to_m_register()
            self.write_code('D=M')
            self.write_pop_to_m_register()
            self.write_code('D=M-D')
            self.write_push_from_d_register()
        elif command == "and":
            self.write_pop_to_m_register()
            self.write_code('D=M')
            self.write_pop_to_m_register()
            self.write_code('D=D&M')
            self.write_push_from_d_register()
        elif command == "or":
            self.write_pop_to_m_register()
            self.write_code('D=M')
            self.write_pop_to_m_register()
            self.write_code('D=D|M')
            self.write_push_from_d_register()
        elif command == "neg":
            self.write_codes([
                '@SP',
                'A=M-1',
                'M=-M'
            ])
        elif command == "not":
            self.write_codes([
                '@SP',
                'A=M-1',
                'M=!M'
            ])
        elif command == "eq":
            self.write_pop_to_m_register()
            self.write_code('D=M')
            self.write_pop_to_m_register()
            l1 = self.get_new_label()
            l2 = self.get_new_label()
            self.write_codes([
                'D=M-D',
                "@%s" % l1,
                'D;JEQ',
                'D=0',
                "@%s" % l2,
                '0;JMP',
                "(%s)" % l1,
                'D=-1',
                "(%s)" % l2,
            ])
            self.write_push_from_d_register()
        elif command == "gt":
            self.write_pop_to_m_register()
            self.write_code('D=M')
            self.write_pop_to_m_register()
            l1 = self.get_new_label()
            l2 = self.get_new_label()
            self.write_codes([
                'D=M-D',
                "@%s" % l1,
                'D;JGT',
                'D=0',
                "@%s" % l2,
                '0;JMP',
                "(%s)" % l1,
                'D=-1',
                "(%s)" % l2,
            ])
            self.write_push_from_d_register()
        elif command == "lt":
            self.write_pop_to_m_register()
            self.write_code('D=M')
            self.write_pop_to_m_register()
            l1 = self.get_new_label()
            l2 = self.get_new_label()
            self.write_codes([
                'D=M-D',
                "@%s" % l1,
                'D;JLT',
                'D=0',
                "@%s" % l2,
                '0;JMP',
                "(%s)" % l1,
                'D=-1',
                "(%s)" % l2,
            ])
            self.write_push_from_d_register()
        else:
            raise Exception("Unknown operator")

    def write_push_pop(self, command, segment, index):
        if command == C_PUSH:
            if segment == "constant":
                self.write_codes([
                    '@%s' % str(index),
                    'D=A',
                    '@SP',
                    'A=M',
                    'M=D',
                    '@SP',
                    'M=M+1'
                ])

    def write_push_from_d_register(self):
        self.write_codes([
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ])

    def write_pop_to_m_register(self):
        self.write_codes([
            '@SP',
            'M=M-1',
            'A=M'
        ])

    def write_code(self, code):
        self.f.write(code + '\n')

    def write_codes(self, codes):
        self.write_code('\n'.join(codes))

    def get_new_label(self):
        self.label_num += 1
        return 'LABEL' + str(self.label_num)
