import os
def load_rom(filename):
    """load instructions to ram"""
    size = os.path.getsize(filename)
    with open(filename, "rb") as rom:
        output = []
        for _ in range(size):
            tmp = rom.read(1).hex()
            if tmp != "":
                output.append(tmp)
        return [int(x,base=16) for x in output]

