

class CodeWriter:
    '''
    Generates assembly code from parsed VM command
    '''

    def __init__(self, out_file):
        self.f = open(out_file, 'w')

    def writeArithmetic(self, command):
        """ 
        Writes to the output file the assembly code that implements the given 
        arithmetic command.
        """
        symbol = self.mathSymbol(command)

        # if neg or not, only get y, and replace with new value; sp stays same
        #  - @SP # go to stack pointer
        #  - A=M-1 # go to where it's pointing minus 1 (y)
        #  - M=-M or !M
        if command == "neg" or command == "not":
            self.f.write("@SP\n")
            self.f.write("A=M-1\n")
            self.f.write("M=" + symbol + "M")

        # for anything else, get x and y, and replace x with the result,
        # then move stack pointer up 1 (y)
        #  - @SP # go to stack pointer
        #  - A=M-1 # go to y
        #  - D=M # get y
        #  - A=A-1 # go to x
        #  - M=D+M, D-M, D&M, D|M
        else:
            self.f.write("@SP\n")
            self.f.write("A=M-1\n")
            self.f.write("D=M\n")
            self.f.write("A=A-1\n")
            self.f.write("M=D" + symbol + "M")

    def writePushPop(self, command, segment, index):
        # Pop: get value from top of stack, move it to segment, move stack down 1
        #  - @index # get the value of the index
        #  - D=A   
        #  - @segment # get address of segment
        #  - M=D+M # Set address to new pop address
        #  - @SP # go to stack pointer
        #  - M=M-1 # Move it up 1
        #  - A=M # go to the value of the m stack
        #  - D=M # get y
        #  - @segment #go to segment pointer
        #  - A=M # Go to pop address
        #  - M=D # pop value

    def mathSymbol(self, command):
        if command == "add":
            return "+"
        elif command == "and":
            return "&"
        elif command == "or":
            return "|"
        elif command == "not":
            return "!"
        else:
            return "-"
        
