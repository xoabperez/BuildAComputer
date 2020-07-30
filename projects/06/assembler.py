#!/usr/bin/python3

from Parser import Parser
from Code import Code
import sys

if len(sys.argv) != 2:
    sys.exit("One argument and one argument only is allowed following assembler.py: the *.asm file to be assembled")
else:
    input_file = sys.argv[1]

output_file = input_file.replace("asm", "hack")
f = open(output_file, 'w')

parser_obj = Parser(input_file)

while parser_obj.hasMoreCommands():
    if parser_obj.commandType() == "C_COMMAND":
        comp = Code.comp(parser_obj.comp())
        jump = Code.jump(parser_obj.jump())        
        dest = Code.dest(parser_obj.dest())
        f.write('111'+comp+dest+jump)
    else:
        f.write(parser_obj.symbol())
    f.write("\n")
    parser_obj.advance()

f.close()
