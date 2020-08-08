#!/usr/bin/python3

from Parser import Parser
from CodeWriter import CodeWriter
import sys

if len(sys.argv) != 2:
    sys.exit("One argument and one argument only is allowed following VMTranslator.py: the *.vm file to be translated")
else:
    input_file = sys.argv[1]

output_file  = input_file.replace("vm", "asm")

parser_obj   = Parser(input_file)
out_file_obj = CodeWriter(output_file)

while parser_obj.hasMoreCommands():
    command = parser_obj.getCommand()
    if parser_obj.commandType() == 'C_ARITHMETIC':
        out_file_obj.writeArithmetic(command)
    else:
        commandType = parser_obj.commandType()
        arg1 = parser_obj.arg1()
        arg2 = parser_obj.arg2()
        out_file_obj.writePushPop(command, commandType, arg1, arg2)
    parser_obj.advance()

out_file_obj.f.close()
