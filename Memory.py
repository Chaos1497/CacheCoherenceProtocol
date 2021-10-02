from time import *

class Memory:
    def __init__(self):
        self.bussy = False
        self.blocks = {}
        for i in range(8):
            self.blocks[f'{i:3b}'.replace(' ', '0')] = f'{0:4X}'.replace(' ', '0')

    def wait(self):
        while self.bussy:
            pass

    def read_block(self, memPos):
        self.bussy = True
        sleep(2)
        self.bussy = False
        return self.blocks[memPos]

    def write_block(self, memPos, data):
        self.bussy = True
        sleep(2)
        self.blocks[memPos] = data
        self.bussy = False

    def view_data(self, x_offset, y_offset):
        view_strings = []
        x = x_offset + 90
        y = y_offset + 130
        div_size = 57
        for i in range(len(self.blocks)):
            data = self.blocks[f'{i:3b}'.replace(' ', '0')]
            view_strings.append({'x': x + (div_size * i), 'y': y , 'string': data})
        return view_strings