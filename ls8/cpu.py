"""CPU functionality."""

import sys

bin_op = {
    0b00000001: 'HLT',
    0b10000010: 'LDI',
    0b01000111: 'PRN',
    0b01000101: 'PUSH',
    0b01000110: 'POP',
    0b01010000: 'CALL',
    0b00010001: 'RET',
    0b01010100: 'JMP',
    0b01010101: 'JEQ',
    0b01010110: 'JNE'
}

math_op = {
    "ADD": 0b10100000,
    "SUB": 0b10100001,
    "MUL": 0b10100010,
    'CMP': 0b10100111
}


sp = 7 #stackpointer
class CPU:
    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.efl = 0
        self.reg[sp] = 0xF4
        self.MAR = None
        self.MDR = None

        self.operand_a = None
        self.operand_b = None
        self.branchtable = {
            'CALL': self.CALL,
            'CMP': self.CMP,
            'HLT': self.HLT,
            'JMP': self.JMP,
            'JEQ': self.JEQ,
            'JNE': self.JNE,
            'LDI': self.LDI,
            'PRN': self.PRN,
            # 'PUSH': self.PUSH,
            # 'POP': self.POP,
            'RET': self.RET,
        }

    def load(self, filename):
        address = 0
        # try:
        f = open(filename)
        for line in f:
            comment_split = line.strip().split("#")
            value = comment_split[0].strip()
            if value == "":
                continue
            instruction = int(value, 2)
            self.ram[address] = instruction
            address += 1
        # except:
        #     print("cant find file")
        #     sys.exit(2)
        address = 0

    def ALU(self, op, reg_a, reg_b):

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == math_op["CMP"]:
                    """Compare the values in two registers."""
                    valueA = self.reg[self.operand_a]
                    valueB = self.reg[self.operand_b]

                    if valueA == valueB:
                        self.FL = 0b00000001

                    if valueA < valueB:
                        self.FL = 0b00000100

                    if valueA > valueB:
                        self.FL = 0b00000010
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
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
    def CALL(self):
        self.reg[sp] -=1
        self.ram[self.reg[sp]] = self.pc +2
        self.pc = self.reg[self.operand_a]

    def RET(self):
        self.pc = self.ram[self.reg[sp]]
        self.reg[sp] += 1
    def CMP(self):
        if self.reg[self.operand_a] == self.reg[self.operand_b]:
            self.efl = 0b00000001
        if self.reg[self.operand_a] < self.reg[self.operand_b]:
            self.efl = 0b00000100
        if self.reg[self.operand_a] > self.reg[self.operand_b]:
            self.efl = 0b00000010
    def JMP(self):
        print("JMP")
        address = self.reg[self.operand_a]
        self.pc = address

    def JEQ(self):
        print("JEQ")
        if self.efl == 1:
            self.pc = self.reg[self.operand_a]
        else:
            self.pc += 2

    def JNE(self):
        print("JNE")

        if self.efl == 0:
            self.pc = self.reg[self.operand_a]

    def HLT(self):
        sys.exit()
    def PRN(self):
        print(self.reg[self.operand_a])

    # def PUSH (self):
    #     global sp
    #     self.reg[sp] -= 1
    #     self.ram[self.reg[pc]] = self.reg[self.operand_a]

    # def POP(self):
    #     global sp
    #     self.reg[self.operand_a] = self.ram[self.reg[sp]]
    #     self.reg[sp] += 1
    def LDI(self):
        print('LDI')
        self.reg[self.operand_a] = self.operand_b

    def move_pc(self, IR):
        #incremnt pc if not set by instruction
        if (IR << 3) % 255 >> 7 != 1:
            self.pc += (IR >> 6) + 1

    def run(self):
        """Run the CPU."""
        while True:
            IR = self.ram_read(self.pc)

            self.operand_a = self.ram_read(self.pc + 1)
            self.operand_b = self.ram_read(self.pc + 2)
            if (IR << 2) % 255 >> 7 == 1: #math op check
                self.ALU(IR, self.operand_a, self.operand_b)
                self.move_pc(IR)
            elif (IR << 2) % 255 >> 7 == 0:
                self.branchtable[bin_op[IR]]()
                self.move_pc(IR)

            else:
                sys.exit(1)

# cpu = CPU()
# cpu.load('./examples/sctest.ls8')
# cpu.run()
