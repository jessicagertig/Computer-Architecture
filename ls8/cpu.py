"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0 # program counter, the address of the current instruction
        self.sp = 0xF4 # stack pointer aka R7 of registef\r
        self.branchtable = {
            LDI: self.ldi,
            PRN: self.prn,
            HLT: self.hlt,
            MUL: self.mul
        }        


    def load(self):
        """Load a program into memory."""

        address = 0

        ##opening a file or program and reading line by line
        ##need to account for sys.argv[1] being left blank
        
        if len(sys.argv) < 2:
            print('No program specified to be run.')
            sys.exit()
        else: 
            with open(sys.argv[1]) as f:
                ##read program file line by line
                for line in f:
                    ##convert to single lines of non-string binary numbers
                    string_val = line.split("#")[0].strip()
                    if string_val == '':
                        continue
                    v = int(string_val, 2)
                    ##set that line of program to current address in ram:
                    self.ram[address] = v
                    ##move to next line in program:
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
        running = True

        
        while running:
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            ##read the mar and store that in the IR
            ir = self.ram_read(self.pc)
            
            if ir in self.branchtable:
                ##if function in branchtable, call function and pass in parameters
                self.branchtable[ir](operand_a, operand_b)
            else:
                print('unknown instruction')
                
            

    def ram_read(self, mar):
        """Return value stored at address (mar) param."""
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        """takes data given to write -MRD- and writes it in address given -MAR-."""
        self.ram[mar] = mdr

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def prn(self, operand_a, operand_b):
        value = self.reg[operand_a]
        print(value)
        self.pc += 2

    def hlt(self, operand_a, operand_b):
        running = False
        sys.exit()

    def mul(self, operand_a, operand_b):
        mult1 = self.reg[operand_a]
        mult2 = self.reg[operand_b]
        result = mult1 * mult2
        self.reg[operand_a] = result
        self.pc +=3