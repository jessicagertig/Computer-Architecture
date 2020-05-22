"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
ADD = 0b10100000
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0 # program counter, the address of the current instruction
        self.sp = 7 # stack pointer aka R7 of register
        self.reg[self.sp] = 0xf4
        self.flag = 6
        self.reg[self.flag] = 0b00000000
        self.branchtable = {
            LDI: self.ldi,
            PRN: self.prn,
            HLT: self.hlt,
            PUSH: self.push,
            POP: self.pop,
            JMP: self.jmp,
            JEQ: self.jeq,
            JNE: self.jne
        }        


    def load(self):
        """Load a program into memory."""

        address = 0

"""TEST CODE"""
        # program = [
        #     0b10000010, # LDI R0,10
        #     0b00000000,
        #     0b00001010,
        #     0b10000010, # LDI R1,20
        #     0b00000001,
        #     0b00010100,
        #     0b10000010, # LDI R2,TEST1
        #     0b00000010,
        #     0b00010011,
        #     0b10100111, # CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010101, # JEQ R2
        #     0b00000010,
        #     0b10000010, # LDI R3,1
        #     0b00000011,
        #     0b00000001,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     0b10000010, # LDI R2,TEST2 # # TEST1 (address 19):
        #     0b00000010,
        #     0b00100000,
        #     0b10100111, # CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010110, # JNE R2
        #     0b00000010,
        #     0b10000010, # LDI R3,2
        #     0b00000011,
        #     0b00000010,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     0b10000010, # LDI R1,10 # TEST2 (address 32):
        #     0b00000001,
        #     0b00001010,
        #     0b10000010, # LDI R2,TEST3
        #     0b00000010,
        #     0b00110000,
        #     0b10100111, # CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010101, # JEQ R2
        #     0b00000010,
        #     0b10000010, # LDI R3,3
        #     0b00000011,
        #     0b00000011,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     0b10000010, # LDI R2,TEST4 ## TEST3 (address 48):
        #     0b00000010,
        #     0b00111101,
        #     0b10100111, # CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010110, # JNE R2
        #     0b00000010,
        #     0b10000010, # LDI R3,4
        #     0b00000011,
        #     0b00000100,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     0b10000010, # LDI R3,5 # TEST4 (address 61):
        #     0b00000011,
        #     0b00000101,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     0b10000010, # LDI R2,TEST5
        #     0b00000010,
        #     0b01001001,
        #     0b01010100, # JMP R2
        #     0b00000010,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     0b00000001, # HLT # TEST5 (address 73):
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

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

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            mult1 = self.reg[reg_a]
            mult2 = self.reg[reg_b]
            result = mult1 * mult2
            self.reg[reg_a] = result
            self.pc +=3
        elif op == CMP:
            num1 = self.reg[reg_a]
            num2 = self.reg[reg_b]
            if num1 == num2:
                self.reg[self.flag] = 0b00000001
            elif num1 < num2: 
                self.reg[self.flag] = 0b00000100
            elif num1 > num2:
                self.reg[self.flag] = 0b00000010
            else:
                self.reg[self.flag] = 0b00000000
            self.pc +=3
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
            mask = ir & 0b00100000
            result = mask >> 5

            if ir in self.branchtable:
                ##if function in branchtable, call function and pass in parameters
                self.branchtable[ir](operand_a, operand_b)
            elif result == 1:
                self.alu(ir, operand_a, operand_b)
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

    def push(self, operand_a, operand_b):
        ##decrement stackpointer
        self.reg[self.sp] -= 1
        ##value to store is located in register at index operand_a as given
        val = self.reg[operand_a]
        ##current top of stack address in ram is value located at address stored at R7 or stack pointer
        top_of_stack_address = self.reg[self.sp]
        ##use ram_write function where mar = address to write to, mdr = value to write to address
        self.ram_write(top_of_stack_address, val)
        
        self.pc +=2
    
    def pop(self, operand_a, operand_b):
        ##need to extract value at current sp location
        val = self.ram_read(self.reg[self.sp])
        ##need to extract reg address to store to 
        ##reg_address = self.reg[operand_a]
        self.reg[operand_a] = val
        ##increment stackpointer
        self.reg[self.sp] += 1
        
        self.pc +=2

    def jmp(self, operand_a, operand_b):
        address = self.reg[operand_a]
        self.pc = address

    def jeq(self, operand_a, operand_b):
        ##if flag is set to equal jump to address stored at given register
        if self.reg[self.flag] == 0b00000001:
            self.jmp(operand_a, operand_b)
        else:
            self.pc +=2
    
    def jne(self, operand_a, operand_b):
        ##if e flag is false, 0, jump to address sorted in given register
        if self.reg[self.flag] != 0b00000001:
            self.jmp(operand_a, operand_b)
        else:
            self.pc +=2