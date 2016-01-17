from constants import *


class CodeWriter():
    def __init__(self, filepath):
        self.f = open(filepath, 'w')
        self.label_num = 0

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.f.close()

    def set_current_translated_file_name(self, file_name):
        self.current_translated_file_name = file_name

    def binary_operation(self, command):
        self.write_pop_to_m_register()
        self.write_code('D=M')
        self.write_pop_to_m_register()
        if command == 'add':
            self.write_code('D=D+M')
        elif command == 'sub':
            self.write_code('D=M-D')
        elif command == 'and':
            self.write_code('D=D&M')
        elif command == 'or':
            self.write_code('D=D|M')
        self.write_push_from_d_register()

    def unary_operation(self, command):
        self.write_codes([
            '@SP',
            'A=M-1',
        ])
        if command == 'neg':
            self.write_code('M=-M')
        elif command == 'not':
            self.write_code('M=!M')

    def comp_operation(self, command):
        self.write_pop_to_m_register()
        self.write_code('D=M')
        self.write_pop_to_m_register()
        l1 = self.get_new_label()
        l2 = self.get_new_label()
        if command == "eq":
            comp_type = "JEQ"
        elif command == "gt":
            comp_type = "JGT"
        elif command == "lt":
            comp_type = "JLT"
        self.write_codes([
            'D=M-D',
            "@%s" % l1,
            'D;%s' % comp_type,
            'D=0',
            "@%s" % l2,
            '0;JMP',
            "(%s)" % l1,
            'D=-1',
            "(%s)" % l2,
        ])
        self.write_push_from_d_register()

    def write_arithmetic(self, command):
        if command in ["add", "sub", "and", "or"]:
            self.binary_operation(command)
        elif command in ["neg", "not"]:
            self.unary_operation(command)
        elif command in ["eq", "gt", "lt"]:
            self.comp_operation(command)

    def write_push_pop(self, command, segment, index):

        index = int(index)

        if command == C_PUSH:
            if segment == "constant":
                self.write_codes([
                    '@%d' % index,
                    'D=A',
                    '@SP',
                    'A=M',
                    'M=D',
                    '@SP',
                    'M=M+1'
                ])
            if segment == "local":
                self.write_codes([
                    '@LCL',
                    'A=M'
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('D=M')
                self.write_push_from_d_register()
            if segment == "argument":
                self.write_codes([
                    '@ARG',
                    'A=M'
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('D=M')
                self.write_push_from_d_register()
            if segment == "this":
                self.write_codes([
                    '@THIS',
                    'A=M'
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('D=M')
                self.write_push_from_d_register()
            if segment == "that":
                self.write_codes([
                    '@THAT',
                    'A=M'
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('D=M')
                self.write_push_from_d_register()
            if segment == "temp":
                self.write_codes([
                    "@%d" % TEMP_BASE_ADDRESS,
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('D=M')
                self.write_push_from_d_register()
            if segment == "pointer":
                self.write_codes([
                    "@%d" % POINTER_BASE_ADDRESS,
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('D=M')
                self.write_push_from_d_register()
            if segment == "static":
                self.write_codes([
                    "@%s.%d" % (self.current_translated_file_name, index),
                ])
                self.write_code('D=M')
                self.write_push_from_d_register()

        elif command == C_POP:
            if segment == "local":
                self.write_pop_to_m_register()
                self.write_codes([
                    'D=M',
                    '@LCL',
                    'A=M'
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('M=D')
            if segment == "argument":
                self.write_pop_to_m_register()
                self.write_codes([
                    'D=M',
                    '@ARG',
                    'A=M'
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('M=D')
            if segment == "this":
                self.write_pop_to_m_register()
                self.write_codes([
                    'D=M',
                    '@THIS',
                    'A=M'
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('M=D')
            if segment == "that":
                self.write_pop_to_m_register()
                self.write_codes([
                    'D=M',
                    '@THAT',
                    'A=M'
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('M=D')
            if segment == "temp":
                self.write_pop_to_m_register()
                self.write_codes([
                    'D=M',
                    '@%d' % TEMP_BASE_ADDRESS,
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('M=D')
            if segment == "pointer":
                self.write_pop_to_m_register()
                self.write_codes([
                    'D=M',
                    '@%d' % POINTER_BASE_ADDRESS,
                ])
                for i in range(index):
                    self.write_code('A=A+1')
                self.write_code('M=D')
            if segment == "static":
                self.write_pop_to_m_register()
                self.write_codes([
                    'D=M',
                    '@%s.%d' % (self.current_translated_file_name, index),
                ])
                self.write_code('M=D')

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
