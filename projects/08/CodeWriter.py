

class CodeWriter:
    '''
    Generates assembly code from parsed VM command
    '''

    def __init__(self, out_file, sys_init):
        ''' 
        Initialize the output file for writing assembly code. Also set up
        some labeled areas for true/false conditions
        '''
        self.out_file = out_file
        self.f = open(out_file, 'w')

        # Bootstrap code sets stack at 256 and does a "call Sys.init 0"
        if sys_init:
            self.f.write("@256\n")
            self.f.write("D=A\n")
            self.f.write("@SP\n")
            self.f.write("M=D\n")
            self.__currentFunction__ = "bootstrap"
            self.__currentReturnNum__ = 0
            self.writeCall("Sys.init", "0", False)
            
        self.__currentComparison__ = 0 # To be used for comparison (gt, lt, eq) return labels

        # Start after setting up gt/lt/eq sections
        self.f.write("@START\n")
        self.f.write("0;JMP\n")

        # Set up sections for gt/lt/eq being true/false
        # 1. Go to SP to go to x (SP-1)
        # 2. Replace with -1/0 for t/f
        # 3. Go to current ROM line pointer
        # 4. Jump back to the correct ROM line

        self.f.write("(IFTRUE)\n")
        self.f.write("@SP\n")
        self.f.write("A=M-1\n") # Move to x to replace
        self.f.write("M=1\n")
        self.f.write("@currentlineP\n") # Go back to procedure
        self.f.write("A=M\n")
        self.f.write("0;JMP\n")

        self.f.write("(IFFALSE)\n")
        self.f.write("@SP\n")
        self.f.write("A=M-1\n")
        self.f.write("M=0\n")
        self.f.write("@currentlineP\n")
        self.f.write("A=M\n")
        self.f.write("0;JMP\n")

        self.f.write("(START)\n")


    def writeArithmetic(self, command):
        """ 
        Writes to the output file the assembly code that implements the given 
        arithmetic command.
        """
        symbol = self.__mathSymbol__(command) # The actual symbol like +, -, etc

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
            
            if command in ["eq", "gt", "lt"]:
                # Set up return label
                self.f.write("@COMP." + str(self.__currentComparison__) + "\n")
                self.f.write("D=A\n")
                self.f.write("@currentlineP\n")
                self.f.write("M=D\n")

                # If there is a comparison, use jumps to go to true/false
                self.f.write("@SP\n")     # Go to x, which now holds x-y
                self.f.write("A=M-1\n")
                self.f.write("D=M\n")
                self.f.write("@IFTRUE\n")
            
                if command == "eq":
                    self.f.write("D;JEQ\n")
                elif command == "gt":
                    self.f.write("D;JGT\n")
                elif command == "lt":
                    self.f.write("D;JLT\n")
            
                self.f.write("@IFFALSE\n")
                self.f.write("0;JMP\n")

                self.f.write("(COMP." + str(self.__currentComparison__) + ")\n")
            
    def __mathSymbol__(self, command):
        '''
        Returns the symbol that will be used for the command operation
        '''
        # For comparisons, neg, and sub, subtract and then use the difference
        if   command == "add": return "+"
        elif command == "and": return "&"
        elif command == "or":  return "|"
        elif command == "not": return "!"
        else:                  return "-"


    def writePushPop(self, command, commandType, segment, index):
        ''' 
        Writes to the output file the assembly code that implements the given
        command, where command is either C_PUSH or C_POP
        '''
        if segment in ["local", "argument", "this", "that"]:
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
            self.f.write("@" + self.filename + "." + str(index) + "\n")
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

    def __segPointer__(self, segment):
        # Gets address of segment pointer for local, argument, this, or that
        if   segment == "local":    return "LCL"
        elif segment == "argument": return "ARG"
        elif segment == "this":     return "THIS"
        elif segment == "that":     return "THAT"


    def writeLabel(self, label):
        '''
        Simply writes the label of a section, so that e.g. "label LOOP"
        becomes "(LOOP)" in assembly
        '''
        self.f.write("(" + label + ")\n")

    def writeGoto(self, label):
        '''
        For an unconditional goto, in assembly we jump to the label. So we write
        the label, then do an unconditional jump.
        '''
        self.f.write("@" + label + "\n")
        self.f.write("0;JMP\n")

    def writeIf(self, label):
        '''
        When there is a comparison, 1 or 0 will be written to the top of the stack.
        We then use this to determine the jump.
        '''
        self.f.write("@SP\n")
        self.f.write("AM=M-1\n")
        self.f.write("D=M\n")
        self.f.write("@" + label + "\n")
        self.f.write("D;JNE\n") # True will be 1, otherwise continue

    def writeFunction(self, functionName, numVars):
        self.__currentFunction__ = functionName
        self.__currentReturnNum__ = 0
        self.f.write("(" + functionName + ")\n") # function label
        for varNum in range(int(numVars)):
            self.f.write("@" + str(varNum) + "\n") # Get var num
            self.f.write("D=A\n")  # Save var num
            self.f.write("@LCL\n") # Go to local pointer
            self.f.write("A=D+M\n")  # Go to var's local address
            self.f.write("M=0\n")  # Initialize to 0
        
        # Move stack pointer past local
        self.f.write("@" + numVars + "\n")
        self.f.write("D=A\n")
        self.f.write("@SP\n")
        self.f.write("M=D+M\n")

    def writeCall(self, functionName, numArgs, returnCall=True):
        # Need at least one arg slot for return value, so move SP up if 0 args
        if numArgs == "0" and returnCall:
            self.f.write("@SP\n")
            self.f.write("M=M+1\n")
            numArgs = "1" # To get correct ARG pointer

        # Get and save return address after args
        self.f.write("@" + self.__currentFunction__ + "$ret." + str(self.__currentReturnNum__) + "\n")
        self.f.write("D=A\n")
        self.f.write("@SP\n")   # Update SP
        self.f.write("M=M+1\n")
        self.f.write("A=M-1\n")
        self.f.write("M=D\n")   # Write return address before SP

        # Save pointers
        for ptr in ["LCL", "ARG", "THIS", "THAT"]:
            self.f.write("@" + ptr + "\n") # Go to pointer
            self.f.write("D=M\n")          # Get address
            self.f.write("@SP\n")          # Go to SP
            self.f.write("M=M+1\n")        # Update SP
            self.f.write("A=M-1\n")
            self.f.write("M=D\n")          # Save ptr before SP

        # Set new pointers
        self.f.write("D=A+1\n")  # Get address of SP
        self.f.write("@" + str(5 + int(numArgs)) + "\n") # slots between SP and ARG
        self.f.write("D=D-A\n") # SP - 5 - numArgs is new ARG address
        self.f.write("@ARG\n")
        self.f.write("M=D\n")
        
        self.f.write("@SP\n")
        self.f.write("D=M\n")
        self.f.write("@LCL\n")
        self.f.write("M=D\n")

        # Start function
        self.f.write("@" + functionName + "\n")
        self.f.write("0;JMP\n")

        # Return function
        self.f.write("(" + self.__currentFunction__ + "$ret." + str(self.__currentReturnNum__) + ")\n")
        self.__currentReturnNum__ += 1


    def writeReturn(self):
        # Move return value to argument 0
        self.f.write("@SP\n")   # Go to stack pointer
        self.f.write("A=M-1\n") # Go to top of stack 
        self.f.write("D=M\n")   # Get latest stack value
        self.f.write("@ARG\n")  # Go to arg pointer
        self.f.write("A=M\n")   # Go to argument 0
        self.f.write("M=D\n")   # Place return value on top of stack
        
        # Move SP
        self.f.write("D=A\n")
        self.f.write("@SP\n")
        self.f.write("M=D+1\n")

        # Save end of frame
        self.f.write("@LCL\n")
        self.f.write("D=M\n")
        self.f.write("@endFrame\n")
        self.f.write("M=D\n")

        # Reset caller's state
        self.f.write("A=M-1\n") # Start with THAT at endFrame-1
        self.f.write("D=M\n")
        self.f.write("@THAT\n")
        self.f.write("M=D\n")

        self.f.write("@2\n")    # THIS at endFrame-2
        self.f.write("D=A\n")
        self.f.write("@endFrame\n")
        self.f.write("A=M-D\n") # Address of saved THIS
        self.f.write("D=M\n")
        self.f.write("@THIS\n")
        self.f.write("M=D\n")     

        self.f.write("@3\n")    # ARG at endFrame-3
        self.f.write("D=A\n")
        self.f.write("@endFrame\n")
        self.f.write("A=M-D\n") # Address of saved ARG
        self.f.write("D=M\n")
        self.f.write("@ARG\n")
        self.f.write("M=D\n")    

        self.f.write("@4\n")    # LCL at endFrame-4
        self.f.write("D=A\n")
        self.f.write("@endFrame\n")
        self.f.write("A=M-D\n") # Address of saved LCL
        self.f.write("D=M\n")
        self.f.write("@LCL\n")
        self.f.write("M=D\n")   

        self.f.write("@5\n")    # Return address at endFrame-5
        self.f.write("D=A\n")
        self.f.write("@endFrame\n")
        self.f.write("A=M-D\n")
        self.f.write("A=M\n")
        self.f.write("0;JMP\n")

    def writeCommand(self, command):
         self.f.write("//"+command+"\n")

    def setFilename(self, filename):
        self.filename = filename

    def close(self):
        self.f.close()