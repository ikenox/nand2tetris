// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// R0: if keyboard is pushed in previous term then 1
// R1: if keyboard is pushed in current term then 1

    // define screen size
    @8192
    D=A
    @number_of_pixel
    M=D

    @R0
    M=0     // Screen is empty at the start
(LOOP)
    @KBD
    D=M
    @KEY_PUSHED
    D;JNE   // if KBD != 0 then goto KEY_PUSHED
(KEY_NOT_PUSHED)
    @R1
    M=0     // R0=0
    @CHECK_STATE_CHANGE
    0;JMP
(KEY_PUSHED)
    @R1
    M=1     // R1=1
(CHECK_STATE_CHANGE)    // if R0 != R1 then screen is update
    @R0
    D=M     // D=R0
    @R1
    D=D-M   // D=R0-R1
    @LOOP
    D;JEQ   // if D == 0 then goto LOOP
    @i
    M=0
    @R1
    D=M
    @R0
    M=D
    @EMPTY_SCREEN_LOOP
    D;JEQ
(FILL_SCREEN_LOOP)
    @i
    D=M
    @number_of_pixel
    D=M-D
    @LOOP
    D;JLT
    @SCREEN
    A=A+D
    M=-1
    @i
    MD=M+1
    @FILL_SCREEN_LOOP
    0;JMP
(EMPTY_SCREEN_LOOP)
    @i
    D=M
    @number_of_pixel
    D=M-D
    @LOOP
    D;JLT
    @SCREEN
    A=A+D
    M=0
    @i
    MD=M+1
    @EMPTY_SCREEN_LOOP
    0;JMP


