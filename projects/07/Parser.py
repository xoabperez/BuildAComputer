

class Parser:
    """
    Encapsulates access to the input code; reads vm commands,
    parses them, and provides access to the commands' components. Also,
    removes all white space and comments.
    """
    
    def __init__(self, file_name):
        """
        Opens the input file and gets ready to parse it
        """
        self.lines = []
        with open(file_name) as f:
            for line in f:
                line = line.replace("\n", "")
                comment = line.find("//")
                # After removing all empty spaces, returns, and comments, anything
                # left is a line to parse (or else it's empty) 
                if comment != -1:
                    line = line[0:comment]
                if len(line) == 0:
                    continue
                self.lines.append(line)
        f.close()

        # Initialize line number to 0
        self.line_num = 0
                
    def hasMoreCommands(self):
        """
        Returns true if there are more commands in the input file
        """
        return self.line_num < self.lines.__len__()

    def advance(self):
        """
        Reads the next command from the input and makes it the current
        command. Should be called only if hasMoreCommands() is true.
        """
        self.line_num += 1

    def getCommand(self):
        self.command = self.lines[self.line_num]
        return self.command

    def commandType(self):
        """
        Returns the type of the current command:
          C_ARITHMETIC: arithmetic/logical commands
          C_PUSH
          C_POP
          C_LABEL
          C_GOTO
          C_IF
          C_FUNCTION
          C_RETURN
          C_CALL
        """
        self.getCommand()
        if   self.command.startswith("push "):     return "C_PUSH"
        elif self.command.startswith("pop "):      return "C_POP"
        elif self.command.startswith("label "):    return "C_LABEL"
        elif self.command.startswith("goto "):     return "C_GOTO"
        elif self.command.startswith("if-goto "):  return "C_IF"
        elif self.command.startswith("function "): return "C_FUNCTION"
        elif self.command.startswith("call "):     return "C_CALL"
        elif self.command.startswith("return "):   return "C_RETURN"
        else:                                      return "C_ARITHMETIC"
    
    def arg1(self):
        '''
        Returns the first argument of the current command. 
        '''
        split_command = self.getCommand().split(" ")
        if self.commandType() == "C_ARITHMETIC":
            return split_command[0]
        else:
            return split_command[1]
            
    def arg2(self):
        split_command = self.getCommand().split(" ")
        return split_command[2]