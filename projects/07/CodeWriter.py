

class CodeWriter:
    '''
    Generates assembly code from parsed VM command
    '''

    def __init__(self, out_file):
        ''' 
        Initialize the output file for writing assembly code. Also set up
        some labeled areas for true/false conditions
        '''
        self.out_file = out_file
        file_name = out_file.split('/')[-1:]
        self.file_name = file_name[0].split('.')[0]

        self.f = open(out_file, 'w')

        # Start after setting up gt/lt/eq sections
        self.f.write("@14\n")
        self.f.write("0;JMP\n")

        # Set up sections for gt/lt/eq being true/false
        # 1. Go to SP to go to x (SP-1)
        # 2. Replace with -1/0 for t/f
        # 3. Go to current line pointer
        # 4. Jump to address being pointed to

        self.iftrue_line_num = "2"       
        self.f.write("@SP\n")
        self.f.write("A=M-1\n") # Move to x to replace
        self.f.write("M=-1\n")
        self.f.write("@currentlineP\n") # Go back to procedure
        self.f.write("A=M\n")
        self.f.write("0;JMP\n")

        self.iffalse_line_num = "8"
        self.f.write("@SP\n")
        self.f.write("A=M-1\n")
        self.f.write("M=0\n")
        self.f.write("@currentlineP\n")
        self.f.write("A=M\n")
        self.f.write("0;JMP\n")


    def __getCurrentLine__(self):
        '''
        Gets the current line number of the output file by closing the file
        first to save contents, opening it to count lines, and then reopening
        it to continue writing to it
        '''
        self.f.close()
        with open(self.out_file) as out_file:
            num_lines = sum(1 for _ in out_file)
        self.f = open(self.out_file, 'a')
        return num_lines


    def writeArithmetic(self, command):
        """ 
        Writes to the output file the assembly code that implements the given 
        arithmetic command.
        """
        self.f.write("//"+command+"\n")
        symbol = self.mathSymbol(command) # The actual symbol like +, -, etc

        # if neg or not, only get y, and replace with new value; sp stays same
        if command == "neg" or command == "not":
            self.f.write("@SP\n")    # Go to stack pointer
            self.f.write("A=M-1\n")  # Go to where it's pointing
            self.f.write("M=" + symbol + "M\n") # Modify it 

        # for anything else, get x and y, and replace x with the result,
        # then move stack pointer up 1 (where y was)
        #  - M=D+M, D-M, D&M, D|M
        else:
            self.f.write("@SP\n")    # Go to stack pointer
            self.f.write("AM=M-1\n") # Move pointer up and go there
            self.f.write("D=M\n")    # Get value of y
            self.f.write("A=A-1\n")  # Go to x
            self.f.write("MD=M" + symbol + "D\n") # Do arithmetic with x(M) and y(D), put in x
            
            # If there is a comparison, save the line to go back to after jumps.
            # Use jumps to go to true/false
            if command == "eq" or command == "gt" or command == "lt":
                self.f.write("@11\n") # Number of lines that will be added to get back to procedure
                self.f.write("D=A\n")
                currentline = str(self.__getCurrentLine__())
                self.f.write("@"+currentline+"\n") 
                self.f.write("D=D+A\n")             # Current line num + 11
                self.f.write("@currentlineP\n")     # Save in this variable
                self.f.write("M=D\n")
                self.f.write("@SP\n")               # Go to x for comparison
                self.f.write("A=M-1\n")
                self.f.write("D=M\n")
                self.f.write("@" + self.iftrue_line_num + "\n")
            
                if command == "eq":
                    self.f.write("D;JEQ\n")
                elif command == "gt":
                    self.f.write("D;JGT\n")
                elif command == "lt":
                    self.f.write("D;JLT\n")
            
                self.f.write("@" +self.iffalse_line_num + "\n")
                self.f.write("0;JMP\n")
            

    def writePushPop(self, command, commandType, segment, index):
        ''' 
        Writes to the output file the assembly code that implements the given
        command, where command is either C_PUSH or C_POP
        '''
        self.f.write("//"+command+"\n")
        if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            seg_name = self.__segPointer__(segment)
            self.f.write("@"+index+"\n") # get the value of the index to add to segment
            self.f.write("D=A\n")        
            self.f.write("@"+seg_name+"\n") # get address of segment
            self.f.write("AD=D+M\n") # save segment address
        elif segment == "constant":
            # for constant, set constant to index
            self.f.write("@" + index + "\n")
            self.f.write("D=A\n")            # For pop, we use D
            self.f.write("@constant\n")
            self.f.write("M=D\n")            # For push, we use M
        elif segment == "static":
            self.f.write("@" + self.file_name + "." + str(index) + "\n")
            self.f.write("D=A\n") # For pop, get address. For push, it'll use M
        elif segment == "temp":
            self.f.write("@" +index +"\n") # Similar situation as for segpointer 
            self.f.write("D=A\n")
            self.f.write("@5\n")
            self.f.write("AD=D+A\n") # Set/save address
        elif segment == "pointer":
            if index == "0":
                self.f.write("@3\n")
            else:
                self.f.write("@4\n")
            self.f.write("D=A\n") 

        if commandType == "C_POP":
            # Pop: get value from top of stack, move it to segment, move stack down 1
            self.f.write("@popto\n")  # Variable point to address where we'll be popping to
            self.f.write("M=D\n")          
            self.f.write("@SP\n")
            self.f.write("AM=M-1\n")  # Move stack up (M), go to y (A)
            self.f.write("D=M\n")     # Get y
            self.f.write("@popto\n")  
            self.f.write("A=M\n")     # Go to where the value will be placed
            self.f.write("M=D\n")     # Set new value
        else:
            # Push: get value from segment, move to top of stack, move stack up 1
            self.f.write("D=M\n")
            self.f.write("@SP\n") # Go to stack
            self.f.write("M=M+1\n")
            self.f.write("A=M-1\n")
            self.f.write("M=D\n") # Push value onto stack

    def mathSymbol(self, command):
        '''
        Returns the symbol that will be used for the command operation
        '''
        # For comparisons, neg, and sub, subtract and then use the difference
        if   command == "add": return "+"
        elif command == "and": return "&"
        elif command == "or":  return "|"
        elif command == "not": return "!"
        else:                  return "-"

    def __segPointer__(self, segment):
        # Gets address of segment pointer for local, argument, this, or that
        if   segment == "local":    return "LCL"
        elif segment == "argument": return "ARG"
        elif segment == "this":     return "THIS"
        elif segment == "that":     return "THAT"

        
