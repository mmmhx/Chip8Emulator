from emulator.utils import *
from emulator.chip import Chip

def main():
    running = True
    test_rom = "tests/1-chip8-logo.ch8"
    rom = load_rom(test_rom)
    chip = Chip(rom)
    chip.load_fontset()
    chip.load_to_memory()
    while (running):
        chip.cpu()
        chip.draw()
        
if __name__ == "__main__":
    main()



