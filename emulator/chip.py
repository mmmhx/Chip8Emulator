import pygame
import math
import random

class Chip:
    def __init__(self, rom):
        self.rom = rom 

    FONTSET = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
    ]

    MEMORY = [0] * 4096 # 4kb ram 
    V      = [0] * 16 
    I      =  0 
    DELAY  =  0
    TIMER  =  0
    PC     =  0x200
    STACK  = [0] * 16
    STACK_PTR = 0
    DISPLAY = [0] * (64 * 32) 
    SCALE = 10

    pygame.init()
    screen = pygame.display.set_mode([64*SCALE, 32*SCALE], vsync=False)
    pygame.display.set_caption("The Simple Chip-8 Emulator")

    def load_fontset(self):
        size = len(self.FONTSET)
        for offset in range(size):
            self.MEMORY[0x80 + offset] = self.FONTSET[offset]


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

            case 0xD000:
                x = self.V[(opcode & 0x0F00) >> 8] % 64
                y = self.V[(opcode & 0x00F0) >> 4] % 64
                n = opcode & 0x000F
                self.V[0xF] = 0
                
                for i in range(n):
                    line = self.MEMORY[self.I + i]
                    for j in range(0,8):
                        pixel = line & (0x80 >> j)
                        if pixel != 0:
                            totalX = x + j
                            totalY = y + i
                            index = totalY * 64 + totalX
                            if self.DISPLAY[index] == 1:
                                self.V[0xF] = 1
                            self.DISPLAY[index] ^= 1

            case _: 
                print(f"{hex(opcode)} NOT IMPLEMENTED YET")



    def draw(self):
        SCALE = self.SCALE
        self.screen.fill('black')
        black = (0,0,0)
        white = (255,255,255)
        clock = pygame.time.Clock()

        for i in range(len(self.DISPLAY)):
            if self.DISPLAY[i] == 1:
                color = white
            if self.DISPLAY[i] == 0:
                color = black

            x = i % 64
            y = math.floor(i / 64)

            rect = pygame.Rect(x * SCALE, y * SCALE , SCALE, SCALE)
            pygame.draw.rect(self.screen, color, rect)
        pygame.display.update()
        clock.tick(60)


