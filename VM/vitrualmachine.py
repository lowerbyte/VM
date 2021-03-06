import struct
import sys

def lbADD(lbvm, *args):
    lbvm.registers[args[0]].r = lbvm.registers[args[0]].r + lbvm.registers[struct.unpack("B",args[1])[0]].r

def lbCMP(lbvm, *args):
    compare = lbvm.registers[args[0]].r - lbvm.registers[args[1]].r
    if compare == 0:
        lbvm.ZF = 1
    if compare < 0:
        lbvm.CF = 1
   
def lbMOV(lbvm, *args):
    lbvm.registers[args[0]].r = lbvm.registers[args[1]].r

def lbSET(lbvm, *args):
    lbvm.registers[args[0]].r = struct.unpack("<H", args[1])[0]

def lbLB(lbvm, *args):
    byte = lbvm.registers[struct.unpack("B",args[1])[0]].r
    lbvm.registers[args[0]].r = byte

def lbSB(lbvm, *args):
    byte = lbvm.registers[args[1]].r
    lbvm.memory.storeByte(lbvm.registers[args[1]].r)
   
def lbOUT(lbvm, *args):
    #This won't be implemented, instead I will use simple print function.
    print(chr(lbvm.memory.mem[lbvm.registers[args[0]].r]))

dir_of_opcodes = {0x00: (lbADD,2), 0x01: (lbCMP, 2), 0x02: (lbMOV, 2), 0x03: (lbSET, 3),
                  0x04: (lbLB, 2), 0x05: (lbSB, 2), 0x10: (lbOUT, 1)}

class LBRegisters:
    def __init__(self):
        self.r = 0

class LBMemory:
    def __init__(self):
        self.mem = bytearray(1048576)

    def storeByte(self, byte, offset):
        self.mem[offset] = byte

    def loadByte(self, offset):
        return self.mem[offset]        

class LBVM:
    def __init__(self):
        self.registers = [LBRegisters() for i in range(10)]
        self.MIP = self.registers[8]
        self.MSP = self.registers[9]
        self.EFLAG = bytearray(8)
        #EFLAG [0   0   0   0   0   0   0   0]
        #                           ^   ^    ^
        #                           |   |    |
        #                           OF  CF   ZF
        self.ZF = self.EFLAG[7]
        self.CF = self.EFLAG[6]
        self.memory = LBMemory()
        self.MIP.r = 0
        self.MSP.r = 500000
        self.offset = 0
    
    def readBytecode(self, filename):
        with open(filename, 'rb') as f:
            for i in f.read():
                self.memory.storeByte(i, self.offset)
                self.offset += 1

    def execute(self, opcode):
        arg1 = self.memory.mem[self.MIP.r+1]
        arg2 = self.memory.mem[self.MIP.r+2 : self.MIP.r+1 + dir_of_opcodes[self.memory.mem[self.MIP.r]][1]]
        func = dir_of_opcodes[self.memory.mem[self.MIP.r]][0]
        func(self, arg1, arg2)
        self.MIP.r +=dir_of_opcodes[self.memory.mem[self.MIP.r]][1]+1

    
    def run(self):
        i = 0
        while i != self.offset:
            self.execute(self.memory.mem)
            i += 1
        sys.exit()

if __name__ == '__main__':
    VM = LBVM()
    VM.readBytecode(sys.argv[1])
    VM.run()


