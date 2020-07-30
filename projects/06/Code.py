

class Code:
    '''
    Translates Hack assembly language mnemonics into binary codes
    '''

    def dest(mn):
        a = '0'
        d = '0'
        m = '0'
        if mn.find('A') != -1:
            a = '1'
        if mn.find('D') != -1:
            d = '1'
        if mn.find('M') != -1:
            m = '1'
        return (a+d+m)

    def comp(mn):
        if mn.find('M') != -1:
            a = '1'
            AorM = 'M'
        else:
            a = '0'
            AorM = 'A'
            
        if mn == '0':
            comp = '101010'
        elif mn == '1':
            comp = '111111'
        elif mn == '-1':
            comp = '111010'
        elif mn == 'D':
            comp = '001100'
        elif mn == AorM:
            comp = '110000'
        elif mn == '!D':
            comp = '001101'
        elif mn == '!' + AorM:
            comp = '110001'
        elif mn == '-D':
            comp = '001111'
        elif mn == '-' + AorM:
            comp = '110011'
        elif mn == 'D+1':
            comp = '011111'
        elif mn == AorM + '+1':
            comp = '110111'
        elif mn == 'D-1':
            comp = '001110'
        elif mn == AorM + '-1':
            comp = '110010'
        elif mn == 'D+' + AorM:
            comp = '000010'
        elif mn == 'D-' + AorM:
            comp = '010011'
        elif mn == AorM + '-D':
            comp = '000111'
        elif mn == 'D&' + AorM:
            comp = '000000'
        else:
            comp = '010101'
        return (a + comp)
    
    def jump(mn):
        if mn == 'JGT':
            return '001'
        elif mn == 'JEQ':
            return '010'
        elif mn == 'JGE':
            return '011'
        elif mn == 'JLT':
            return '100'
        elif mn == 'JNE':
            return '101'
        elif mn == 'JLE':
            return '110'
        elif mn == 'JMP':
            return '111'
        else:
            return '000'
        
