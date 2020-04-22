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
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256

    def load(self, filename):
        address = 0
        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.strip().split("#")
                    value = comment_split[0].strip()
                    if value == "":
                        continue
                    instruction = int(value, 2)
                    self.ram[address] = instruction
                    address += 1
        except:
            print("cant find file")
            sys.exit(2)
        address = 0


        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

    def alu(self, op, reg_a, reg_b):

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
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
    def run(self):

        while True:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == HLT:
                break
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == MUL:
                self.alu(IR, operand_a, operand_b)
                self.pc += 3
            else:
                print("Error")
                exit()
