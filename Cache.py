from threading import *
from random import *

class Cache:
    def __init__(self, n, bus):
        Thread.__init__(self)
        self.id = n
        self.bus = bus
        self.blocks = []
        for i in range(4):
            index = 0
            if i > 1:
                index = 1
            self.blocks.append({'ID': f'{i:2b}'.replace(' ', '0'), 'STATUS': 'I', 'MEMPOS': f'{0:3b}', 'INDEX': f'{index:1b}'.replace(' ', '0'), 'DATA': f'{0:4X}'.replace(' ', '0')})

    def block_in_memory(self, memPos):
        for n in range(len(self.blocks)):
            if memPos[-1] == self.blocks[n]['INDEX']:
                if memPos == self.blocks[n]['MEMPOS']:
                    if self.blocks[n]['STATUS'] != 'I':
                        return True
        return False

    def write_block(self, memPos, data):
        for n in range(len(self.blocks)):
            if memPos[-1] == self.blocks[n]['INDEX']:
                if memPos == self.blocks[n]['MEMPOS']:
                    self.blocks[n]['DATA'] = data

    def read_block(self, memPos):
        for n in range(len(self.blocks)):
            if memPos[-1] == self.blocks[n]['INDEX']:
                if memPos == self.blocks[n]['MEMPOS']:
                    return self.blocks[n]['DATA']

    def get_block_status(self, memPos):
        for n in range(len(self.blocks)):
            if memPos[-1] == self.blocks[n]['INDEX']:
                if memPos == self.blocks[n]['MEMPOS']:
                    return self.blocks[n]['STATUS']

    def set_block_status(self, memPos, status):
        for n in range(len(self.blocks)):
            if memPos[-1] == self.blocks[n]['INDEX']:
                if memPos == self.blocks[n]['MEMPOS']:
                    self.blocks[n]['STATUS'] = status

    def replace_block(self, memPos, data):
        random_field = randint(0, 4)
        for n in range(len(self.blocks)):
            if memPos[-1] == self.blocks[n]['INDEX']:
                if n % 2 == random_field:
                    if self.blocks[n]['STATUS'] == 'M':
                        self.bus.writeThrough(self.blocks[n]['MEMPOS'] + self.blocks[n]['INDEX'], self.blocks[n]['DATA'])
                    self.blocks[n]['MEMPOS'] = memPos
                    self.blocks[n]['DATA'] = data

    def process_cpu_read_hit(self, memPos):
        if not self.block_in_memory(memPos):
            data = self.bus.readMiss(self.id, memPos)
            self.replace_block(memPos, data['DATA'])
            if data['SHARED']:
                self.set_block_status(memPos, 'S')
            else:
                self.set_block_status(memPos, 'E')

    def process_cpu_write_hit(self, memPos, data):
        if self.block_in_memory(memPos):
            block_status = self.get_block_status(memPos)
            if block_status in ['S', 'O']:
                self.bus.invalidate(self.id, memPos)
            self.write_block(memPos, data)
        else:
            self.replace_block(memPos, data)
            self.bus.writeMiss(self.id, memPos)
        self.set_block_status(memPos, 'M')

    def process_bus_read_miss(self, memPos):
        if self.block_in_memory(memPos):
            block_status = self.get_block_status(memPos)
            if block_status == 'M':
                data = self.read_block(memPos)
                self.bus.writeThrough(memPos, data)
                self.set_block_status(memPos, 'O')
                #print("Read miss en ", memPos, "\n")
            if block_status == 'E':
                self.set_block_status(memPos, 'S')
                #print("Read miss en ", memPos, "\n")
            return self.read_block(memPos)
        return None

    def process_bus_write_miss(self, memPos):
        if self.block_in_memory(memPos):
            block_status = self.get_block_status(memPos)
            if block_status == 'M':
                data = self.read_block(memPos)
                self.bus.writeThrough(memPos, data)
            self.set_block_status(memPos, 'I')
            #print("Write miss en ", memPos, "\n")