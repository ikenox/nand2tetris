#!/usr/bin/python
# -*- coding: utf-8 -*-

from constants import *
from parser import Parser
from code_writer import CodeWriter
import glob
import argparse


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('path', type=str, help='vm file or folder')

    args = parser.parse_args()
    path = args.path

    if path.endswith(".vm"):
        with CodeWriter(path[:-3] + ".asm") as code_writer:
            translate_file(path, code_writer)
        print path[:-3] + ".asm"
    else:
        if path.endswith("/"):
            path = path[:-1]
        with CodeWriter(path + ".asm") as code_writer:
            files = glob.glob("%s/*" % path)
            for file in files:
                if file.endswith(".vm"):
                    translate_file(file, code_writer)
        print path + ".asm"


def translate_file(file, code_writer):
    with Parser(file) as parser:
        parser.advance()
        while parser.current_command != None:
            if parser.command_type() == C_ARITHMETIC:
                code_writer.write_arithmetic(parser.arg1())
            elif parser.command_type() == C_PUSH:
                code_writer.write_push_pop(C_PUSH, parser.arg1(), parser.arg2())
            elif parser.command_type() == C_POP:
                pass

            parser.advance()



if __name__ == '__main__':
    main()
