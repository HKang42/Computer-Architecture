"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, reg = [0] * 8, pc = 0):
        """Construct a new CPU."""
        self.reg = reg # register
        self.ram = [0] * 256 # RAM
        self.pc = pc # program counter

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]


        # Loop through each instruction and store it in memory
        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # After loading a program, we want to run it.
        running = True
        while running == True:

            # LDI instruction
            if self.ram_read(self.pc) == 0b10000010:
                """
                LDI register immediate
                Set the value of a register to an integer.

                [command] = 0b10000010
                [register number]
                [immediate value]
                """

                register_num = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)

                self.reg[register_num] = value
                self.pc += 3
            
            elif self.ram_read(self.pc) == 0b01000111:
                """
                `PRN register` pseudo-instruction
                Print numeric value stored in the given register.

                [command] = 0b01000111
                [register number]
                """
                register_num = self.ram_read(self.pc + 1)
                
                print(self.reg[register_num])
                self.pc += 2

            elif self.ram[self.pc] == 0b00000001:
                """
                `HLT`
                Halt the CPU (and exit the emulator).

                [command] = 0b00000001
                """
                running = False
                

        

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
