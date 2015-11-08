// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    @R2
    M=0     // R2 = 0
    @i
    M=1     // i = 1
(LOOP)
    @i
    D=M     // D = i
    @R1     
    D=D-M   // D = i - R1
    @END
    D;JGT   // if D > 0 then goto END
    @R0
    D=M     // D = R0
    @R2
    M=D+M   // R2 += R0
    @i
    M=M+1   // i++
    @LOOP
    0;JMP   // Goto LOOP
(END)
    @END
    0;JMP   // Goto END (infinite loop)