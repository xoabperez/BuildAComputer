

class Parser:
    """
    Encapsulates access to the input code; reads an assembly command,
    parses it, and provides access to the command's components. Also,
    removes all white space and comments.
    """

    def __init__(self, file_name):
        """
        Opens the input file and gets ready to parse it
        """
        self.lines = []
        with open(file_name) as f:
            for line in f:
                line = line.replace(" ", "")
                line = line.replace("\n", "")
                comment = line.find("//")
                if comment != -1:
                    line = line[0:comment]
                if len(line) == 0:
                    continue
                self.lines.append(line)
        f.close()

        self.line_num = 0
        self.command = self.lines[self.line_num]
                
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

    def commandType(self):
        """
        Returns the type of the current command:
          A_COMMAND for @xxx, where xxx is either a symbol or decimal number
          C_COMMAND for dest=comp;jump
          L_COMMAND for (xxx), where xxx is a symbol
        """
        self.command = self.lines[self.line_num]
        if self.command.startswith("@"):
            return "A_COMMAND"
        elif self.command.startswith("("):
            return "L_COMMAND"
        else:
            return "C_COMMAND"
    
    def symbol(self):
        """
        Returns the symbol or decimal xxx of the current command, @xxx or (xxx)
        Should be called only when commandType() is A or L
        """
        return self.command.strip("(@)") 

    def dest(self):
        """
        Returns the dest mnemonic in the current C-command (8 possibilities)
        Should be called only when commandType() is C
         """
        if self.command.find('=') != -1:
            parts = self.command.split('=')
        else:
            parts = ['']
        return parts[0]

    def comp(self):
        """
        Returns the comp mnemonic in the current C-command (28 possibilities)
        Should be called only when commandType is C
        """
        if self.command.find('=') != -1:
            parts = self.command.split('=')
        elif self.command.find(';') != -1:
            parts = self.command.split(';')
            parts.insert(0,'')
        else:
            parts = ['',''];
        return parts[1]


    def jump(self):
        """
        Returns the jump mnemonic in the current C-command (8 possibilities)
        Should be called only when commandType is C
        """
        if self.command.find(';') != -1:
            parts = self.command.split(';')
        else:
            parts = ['',''];
        return parts[1]

