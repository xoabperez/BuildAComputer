#!/usr/bin/python3

from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable
import sys

if len(sys.argv) != 2:
    sys.exit("One argument and one argument only is allowed following assembler.py: the *.asm file to be assembled")
else:
    input_file = sys.argv[1]

output_file = input_file.replace("asm", "hack")
f = open(output_file, 'w')

parser_obj = Parser(input_file)
table_obj = SymbolTable()
assembled_line_num = 0 # line number of lines that will be assembled (not labels)

# First pass - find all labels and add to symbol table
while parser_obj.hasMoreCommands():
    if parser_obj.commandType() == "L_COMMAND":
        symbol = parser_obj.symbol()
        table_obj.addEntry(symbol, assembled_line_num) # all labels are new
        assembled_line_num -= 1 # this line won't be assembeled
    assembled_line_num += 1
    parser_obj.advance()

# Second pass - exchange variable names for values and assemble        
parser_obj.line_num = 0
avail_address = 16    
while parser_obj.hasMoreCommands():
    if parser_obj.commandType() == "C_COMMAND":
        comp = Code.comp(parser_obj.comp())
        jump = Code.jump(parser_obj.jump())        
        dest = Code.dest(parser_obj.dest())
        f.write('111'+comp+dest+jump)
    elif parser_obj.commandType() == "A_COMMAND":
        symbol = parser_obj.symbol()        
        try:
            value = int(symbol)
        except:
            if table_obj.containsKey(symbol):
                value = table_obj.getAddress(symbol)
            else:
                table_obj.addEntry(symbol, avail_address)
                value = avail_address
                avail_address += 1
        py_bin_str = bin(value)
        bin_str = py_bin_str[2:]
        num_zeros = 16-len(bin_str)
        bin_str = (num_zeros*'0'+bin_str)
        f.write(bin_str)
    else:
        parser_obj.advance()
        continue

    f.write("\n")
    parser_obj.advance()

f.close()
