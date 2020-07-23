// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

	// Initialize total to 0
	@R2
	M=0

	// Check which variable is larger; iterate over smaller, add larger
	@R0
	D=M
	@R1
	D=D-M // R0-R1
	@FIRSTBIGGER
	D;JGT 
	@SECONDBIGGER
	0;JMP

(FIRSTBIGGER) 
	@R1
	D=M
	@iterator
	M=D

	@R0
	D=M
	@adder
	M=D

	@LOOP
	0;JMP

(SECONDBIGGER) 
	@R0
	D=M
	@iterator
	M=D

	@R1
	D=M
	@adder
	M=D

	@LOOP
	0;JMP
		
(LOOP)
	@iterator // Stop when this is zero; otherwise, subtract 1
	D=M
	@END
	D;JEQ
	@iterator
	M=M-1
	
	@adder // Add the adder value to the total
	D=M
	@R2
	M=D+M

	@LOOP // And continue the loop
	0;JMP

(END)
	@END
	0;JMP
