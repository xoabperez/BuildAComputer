#!/usr/bin/python3

from Parser import Parser
from CodeWriter import CodeWriter
import sys

if len(sys.argv) != 2:
    sys.exit("One argument and one argument only is allowed following VMTranslator.py: the *.vm file to be translated")
else:
    input_file = sys.argv[1]

output_file = input_file.replace("vm", "asm")
out_file_obj = CodeWriter(output_file)

parser_obj = Parser(input_file)
assembled_line_num = 0 # line number of lines that will be assembled (not labels)

# First pass - find all labels and add to symbol table
while parser_obj.hasMoreCommands():
    if parser_obj.commandType() == "L_COMMAND":
        assembled_line_num -= 1 # this line won't be assembeled
    assembled_line_num += 1
    parser_obj.advance()

out_file_obj.f.close()
