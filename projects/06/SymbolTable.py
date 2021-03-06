

class SymbolTable:
    """
    Keeps a correspondence between symbolic labels and numeric addresses.
    """

    def __init__(self):
        """
        Creates a new empty symbol table
        """
        self.table = dict(SP=0, LCL=1, ARG=2, THIS=3, THAT=4, R0=0, R1=1, R2=2, R3=3, R4=4, R5=5, R6=6, R7=7, R8=8, R9=9, R10=10, R11=11, R12=12, R13=13, R14=14, R15=15, SCREEN=16384, KBD=24576)

    def addEntry(self, symbol, address):
        """
        Adds the pair {symbol:address} to the table
        """
        self.table[symbol] = address

    def containsKey(self, symbol):
        """
        Returns whether the table contains the given symbol
        """
        return symbol in self.table

    def getAddress(self, symbol):
        """
        Returns the address associated with the symbol
        """
        return self.table[symbol]

    def containsValue(self, value):
        return value in self.table.values()
