@14
0;JMP
@SP
A=M-1
M=-1
@currentlineP
A=M
0;JMP
@SP
A=M-1
M=0
@currentlineP
A=M
0;JMP
@111
D=A
@constant
M=D
D=M
@SP
M=M+1
A=M-1
M=D
@333
D=A
@constant
M=D
D=M
@SP
M=M+1
A=M-1
M=D
@888
D=A
@constant
M=D
D=M
@SP
M=M+1
A=M-1
M=D
@StaticTest.8
D=A
@popto
M=D
@SP
AM=M-1
D=M
@popto
A=M
M=D
@StaticTest.3
D=A
@popto
M=D
@SP
AM=M-1
D=M
@popto
A=M
M=D
@StaticTest.1
D=A
@popto
M=D
@SP
AM=M-1
D=M
@popto
A=M
M=D
@StaticTest.3
D=A
D=M
@SP
M=M+1
A=M-1
M=D
@StaticTest.1
D=A
D=M
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
A=A-1
MD=M-D
@StaticTest.8
D=A
D=M
@SP
M=M+1
A=M-1
M=D
@SP
AM=M-1
D=M
A=A-1
MD=M+D
