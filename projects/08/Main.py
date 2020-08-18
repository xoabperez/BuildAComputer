#!/usr/bin/python3

from Parser import Parser
from CodeWriter import CodeWriter
import sys
import os

if len(sys.argv) != 2:
    sys.exit("One argument and one argument only is allowed following VMTranslator.py: the *.vm file to be translated")
else:
    input_file_or_dir = sys.argv[1]

if os.path.isdir(input_file_or_dir):
    vm_filenames = [f for f in os.listdir(input_file_or_dir) if f.endswith(".vm")]
    vm_fullpaths = [input_file_or_dir + f for f in vm_filenames] 

    dir_name = input_file_or_dir.split(os.path.sep)[-2] # Ends with "/" so there will be empty string at -1
    output_file = input_file_or_dir + dir_name + ".asm" # Name .asm after the directory

    sys_init = True # For directories, need to bootstrap and call sys_init

elif os.path.isfile(input_file_or_dir):
    vm_fullpaths = [input_file_or_dir]
    output_file = input_file_or_dir.replace("vm", "asm")
    sys_init = False

# Open and initialize output file
out_file_obj = CodeWriter(output_file, sys_init)

# For directories, we'll translate all files into a single assembly file
for input_file in vm_fullpaths:
    parser_obj = Parser(input_file)

    # Will need filename for static variables
    filename = input_file.split(os.path.sep)[-1]
    filename = filename.split(".")[0]
    out_file_obj.setFilename(filename)

    while parser_obj.hasMoreCommands():
        command = parser_obj.getCommand()
        commandType = parser_obj.commandType()
        out_file_obj.writeCommand(command)
        
        if commandType == 'C_RETURN':
            out_file_obj.writeReturn()
        elif (commandType == 'C_PUSH') or (commandType == 'C_POP') \
            or (commandType == 'C_FUNCTION') or (commandType == 'C_CALL'):
            arg1 = parser_obj.arg1()
            arg2 = parser_obj.arg2()
            if commandType == "C_FUNCTION":
                out_file_obj.writeFunction(arg1, arg2)
            elif commandType == "C_CALL":
                out_file_obj.writeCall(arg1, arg2)
            else:
                out_file_obj.writePushPop(command, commandType, arg1, arg2)
        else:
            arg1 = parser_obj.arg1()
            if commandType == "C_LABEL":
                out_file_obj.writeLabel(arg1)
            elif commandType == "C_GOTO":
                out_file_obj.writeGoto(arg1)
            elif commandType == "C_IF":
                out_file_obj.writeIf(arg1)
            elif commandType == 'C_ARITHMETIC':
                out_file_obj.writeArithmetic(arg1)

        parser_obj.advance()

out_file_obj.close()
