class Chip:
    def __init__(self, rom):
        self.rom = rom 
    MEMORY = [0] * 4096 # 4kb ram 
    V      = [0] * 16 
    I      =  0 
    DELAY  =  0
    TIMER  =  0
    PC     =  0x200
    STACK  = [0] * 16
    STACK_PTR = 0
    DISPLAY = [0] * (64 * 32) 

    def load_to_memory(self):
        size = len(self.rom)
        for offset in range(size):
            self.MEMORY[0x200 + offset] = self.rom[offset]

    def cpu(self):
        opcode = (self.MEMORY[self.PC] << 8) | (self.MEMORY[self.PC + 1])
        self.PC += 2
        match (opcode & 0xF000):
            case 0x0000:
                opcode = opcode & 0x00FF
                match (opcode):
                    case 0x00E0:
                        DISPLAY = [0] * (64 * 32) 
                        print("CLS")
                    case 0x00EE:
                        self.PC = self.STACK[self.STACK_PTR]
                        self.STACK_PTR -= 1
                        print(f"RET, {self.PC}")    

            case 0x1000:
                nnn = opcode & 0x0FFF
                self.PC = nnn
                print(f"JP, {nnn}")



            case 0xA000:
                nnn = opcode & 0x0FFF
                self.I = nnn
                print(f"LD I, {nnn}")


            case 0x6000:
                x = (opcode & 0x0F00) >> 8
                kk = opcode & 0x00FF
                self.V[x] = kk
                print(f"LD, V{x} {kk}")

            case _: 
                print(f"{hex(opcode)} NOT IMPLEMENTED YET")
   

