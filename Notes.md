Need to impliment an emulator for the world-famous LambdaSchool-8 computer (LS-8) 
 - This is an 8-bit computer with 8-bit memory addressing
    - computer uses 8-bit instructions/values
    - memory contains 8-bit instructions/values
 - About as simple as it gets.

we have 8 registers. each register stores only 8-bit numbers 

 An 8 bit CPU is one that only has 8 wires available for addresses (specifying where something is in memory), computations, and instructions. With 8 bits, our CPU has a total of 256 bytes of memory and can only compute values up to 255. The CPU could support 256 instructions, as well, but we won't need them.


Goal is to fill out the CPU class (constructor) so that it can load and run a program.
 - To make starting easier, the program has been hardcoded into the load method
 - For day 1, the hardcoded program is to print the number 8


For our memory (RAM), we have 256 addresses. Each address can read or write one 8-bit value
 - https://www.youtube.com/watch?v=fpnE6UAfbtU


## Registers

8 general-purpose 8-bit numeric registers R0-R7.

* R5 is reserved as the interrupt mask (IM)
* R6 is reserved as the interrupt status (IS)
* R7 is reserved as the stack pointer (SP)

> These registers only hold values between 0-255. After performing math on
> registers in the emulator, bitwise-AND the result with 0xFF (255) to keep the
> register values in that range.


## Internal Registers

* `PC`: Program Counter, address of the currently executing instruction
* `IR`: Instruction Register, contains a copy of the currently executing instruction
* `MAR`: Memory Address Register, holds the memory address we're reading or writing
* `MDR`: Memory Data Register, holds the value to write or the value just read
* `FL`: Flags, see below


## Power on State

When the LS-8 is booted, the following steps occur:

* `R0`-`R6` are cleared to `0`.
* `R7` is set to `0xF4`.
* `PC` and `FL` registers are cleared to `0`.
* RAM is cleared to `0`.

Subsequently, the program can be loaded into RAM starting at address `0x00`.


## Execution Sequence

1. The instruction pointed to by the `PC` is fetched from RAM, decoded, and
   executed.
2. If the instruction does _not_ set the `PC` itself, the `PC` is advanced to
   point to the subsequent instruction.
3. If the CPU is not halted by a `HLT` instruction, go to step 1.

Some instructions set the PC directly. These are:

* CALL
* INT
* IRET
* JMP
* JNE
* JEQ
* JGT
* JGE
* JLT
* JLE
* RET

In these cases, the `PC` does not automatically advance to the next instruction,
since it was set explicitly.


## Instruction Layout

Meanings of the bits in the first byte of each instruction: `AABCDDDD`

* `AA` Number of operands for this opcode, 0-2
* `B` 1 if this is an ALU operation
* `C` 1 if this instruction sets the PC
* `DDDD` Instruction identifier

The number of operands `AA` is useful to know because the total number of bytes in any
instruction is the number of operands + 1 (for the opcode). This
allows you to know how far to advance the `PC` with each instruction.

It might also be useful to check the other bits in an emulator implementation, but
there are other ways to code it that don't do these checks.