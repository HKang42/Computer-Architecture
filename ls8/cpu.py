"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):#, reg = [0] * 8, pc = 0, sp = None):
        """Construct a new CPU."""
        self.reg = [0] * 8      # General Purpose Registers
        self.ram = [0] * 256    # RAM
        self.sp = self.reg[7]  # Stack Pointer
        
        # Internal Registers
        self.pc = 0             # Program Counter
        self.ir = 0b00000001    # Instruction register (defaults to halt)

    def load(self):
        """Load a program into memory."""

        address = 0

        # Make sure a program file has been provided
        if len(sys.argv) != 2:
            print("Please provide a valid program file (e.g. cpu.py print8.ls8)")
            sys.exit(1)

        # Load file and write contents to memory (self.ram)
        program_file = 'examples/' + sys.argv[1] + '.ls8'
        try:
            with open(program_file) as f:
                for line in f:
                    try:
                        line = line.split("#", 1)[0]
                        line = int(line, 2)
                        self.ram_write(address, line)
                        address += 1
                    
                    # skip empty lines and lines without numbers
                    except ValueError:
                        pass
        
        # If file cannot be found
        except FileNotFoundError:
            print('File "{}" not found'.format(program_file))
            sys.exit(1)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

        elif op == 'MUL':
            return self.reg[reg_a] * self.reg[reg_b]

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


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value


    def pc_increment(self, instruction):
        """
        Given an instruction, return the number PC must be incremented by 
        after that instruction has been run
        """
        
        # Use a mask with 
        mask = 0b11000000
        
        # Remove irrelevant information with mask
        operands = instruction & mask

        # Shift bits to remove trailing 0's
        operands = operands >> 6

        # Add one to account for the instruction itself
        return operands + 0b1

    def run(self):
        """Run the CPU."""
        
        self.reg[7] = 0xF4
        # After loading a program, we want to run it.
        running = True
        
        while running == True:
            instruction = self.ram_read(self.pc)
            self.ir = instruction
            
            # LDI 
            if instruction == 0b10000010:
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
                self.pc += self.pc_increment(instruction)
                
            
            # PRN
            elif instruction == 0b01000111:
                """
                `PRN register` pseudo-instruction
                Print numeric value stored in the given register.

                [command] = 0b01000111
                [register number]
                """
                register_num = self.ram_read(self.pc + 1)
                
                print(self.reg[register_num])
                self.pc += self.pc_increment(instruction)

            # HLT
            elif instruction == 0b00000001:
                """
                `HLT`
                Halt the CPU (and exit the emulator).

                [command] = 0b00000001
                """
                running = False
            
            ### Stack Operations
            # PUSH
            elif instruction == 0b01000101:
                """
                `PUSH`
                Push the value in the given register on the stack.
                1. Decrement the `SP`.
                2. Copy the value in the given register to the address pointed to by `SP`.

                [command] = 01000101
                [register number]
                """
                # Step 1
                self.sp -= 1

                # Step 2
                register_num = self.ram_read(self.pc + 1)
                value = self.reg[register_num]
                self.ram_write(self.sp, value)
                
                self.pc += self.pc_increment(instruction)
            
            # POP
            elif instruction == 0b01000110:
                """
                `POP register`
                Pop the value at the top of the stack into the given register.
                1. Copy the value from the address pointed to by `SP` to the given register.
                2. Increment `SP`.

                [command] = 01000110
                [register number]
                """
                # Step 1
                value = self.ram_read(self.sp)

                register_num = self.ram_read(self.pc + 1)
                self.reg[register_num] = value
                
                # Step 2
                self.sp += 1

                self.pc += self.pc_increment(instruction)

            ### Arithmetic Operations
            # ADD
            elif instruction == 0b10100000:
                pass
            
            # MUL
            elif instruction == 0b10100010:
                """
                `MUL registerA registerB`
                Multiply the values in two registers together and store the result in registerA.

                [command] = 0b10100010
                [register number A]
                [register number A]
                """
                register_num_A = self.ram_read(self.pc + 1)
                register_num_B = self.ram_read(self.pc + 2)
                product = self.alu('MUL', register_num_A, register_num_B)
                
                self.reg[register_num_A] = product
                self.pc += self.pc_increment(instruction)
            
            # SUB
            elif instruction == 0b10100001:
                """
                `SUB registerA registerB`

                Subtract the value in the second register from the first, storing the
                result in registerA.

                Machine code:
                ```
                10100001 00000aaa 00000bbb
                """
                pass
            
            # DIV
            elif instruction == 10100011:
                """
                `DIV registerA registerB`
                Divide the value in the first register by the value in the second,
                storing the result in registerA.
                If the value in the second register is 0, the system should print an
                error message and halt.

                Machine code:
                ```
                10100011 00000aaa 00000bbb
                """
                pass

        
