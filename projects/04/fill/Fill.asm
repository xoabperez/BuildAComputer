// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

	@previousval // initialize to everything white
	M=0

(KEYCHK) // Continuously check if keyboard has been clicked (value !=0)
	@KBD
	D=M
	@NOCLICK
	D;JEQ
	@CLICK
	0;JMP

(NOCLICK) // If no click, check if it was black before; if so, whiten
	@previousval
	D=M
	@WHITEN
	D;JNE // if not equal to zero, it was black before
	@KEYCHK
	D;JMP

(CLICK) // If click, check if it was white before; if so, blacken
	@previousval
	D=M
	@BLACKEN
	D;JEQ
	@KEYCHK
	D;JMP

(WHITEN) // Set color to 0 and paint with it
	@color
	M=0
	@previousval // previous value will be white
	M=0
	@STARTPAINT
	0;JMP

(BLACKEN) // Set color to -1 and paint with it
	@color
	M=-1
	@previousval // previous value is non-white
	M=1
	@STARTPAINT
	0;JMP

(STARTPAINT) // Set up first register to SCREEN, then loop
	@SCREEN
	D=A
	@screenreg
	M=D
	@PAINTLOOP
	0;JMP

(PAINTLOOP)
	@KBD
	D=A
	@screenreg
	D=D-M
	@KEYCHK // Stop once we arrive at the kbd
	D;JEQ
	@color
	D=M
	@screenreg
	A=M
	M=D
	@screenreg
	M=M+1
	@PAINTLOOP
	0;JMP

	
