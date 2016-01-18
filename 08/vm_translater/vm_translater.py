#!/usr/bin/python
# -*- coding: utf-8 -*-

from constants import *
from parser import Parser
from code_writer import CodeWriter
import glob
import argparse
import os.path


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('path', type=str, help='vm file or folder')

    args = parser.parse_args()
    path = args.path

    if path.endswith(".vm"):  # file
        with CodeWriter(path[:-3] + ".asm") as code_writer:
            translate_file(path, code_writer)
        print "Translated to", path[:-3] + ".asm"
    else:  # directory
        if path.endswith("/"):
            path = path[:-1]
        with CodeWriter(path + "/" + os.path.basename(path) + ".asm") as code_writer:
            files = glob.glob("%s/*" % path)
            for file in files:
                if file.endswith(".vm"):
                    translate_file(file, code_writer)
        print "Translated to", path + "/" + os.path.basename(path) + ".asm"


def translate_file(file, code_writer):
    filename, _ = os.path.splitext(os.path.basename(file))
    code_writer.set_current_translated_file_name(filename)
    with Parser(file) as parser:
        parser.advance()
        while parser.current_command != None:

            code_writer.write_code("// "+" ".join(parser.current_command))

            if parser.command_type() == C_ARITHMETIC:
                code_writer.write_arithmetic(parser.arg1())
            elif parser.command_type() == C_PUSH:
                code_writer.write_push_pop(C_PUSH, parser.arg1(), parser.arg2())
            elif parser.command_type() == C_POP:
                code_writer.write_push_pop(C_POP, parser.arg1(), parser.arg2())
            elif parser.command_type() == C_LABEL:
                code_writer.write_named_label(parser.arg1())
            elif parser.command_type() == C_GOTO:
                code_writer.write_goto(parser.arg1())
            elif parser.command_type() == C_IF:
                code_writer.write_if(parser.arg1())
            elif parser.command_type() == C_FUNCTION:
                code_writer.write_function(parser.arg1(), parser.arg2())
            elif parser.command_type() == C_RETURN:
                code_writer.write_return()
            elif parser.command_type() == C_CALL:
                code_writer.write_call(parser.arg1(),parser.arg2())
            parser.advance()


if __name__ == '__main__':
    main()
