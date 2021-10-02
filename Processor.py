from time import *
from math import *
from copy import *
from Cache import *

class Processor(Thread):
    def __init__(self, n, bus):
        Thread.__init__(self)
        self.id = n
        self.bus = bus
        self.cache = Cache(n, bus)
        self.bus.connecting(self.cache)
        self.prev_inst = {'INST': '', 'OP1': '', 'OP2': ''}
        self.curr_isnt = {'INST': '', 'OP1': '', 'OP2': ''}
        self.forced_isnt = {'INST': '', 'OP1': '', 'OP2': ''}
        self.forced = False
        self.pause = True
        self.steps = -2
        self.next = False

    def poisson(self, lamb, k):
        return (pow(lamb,k)*exp(-lamb))/factorial(k)

    def random_poisson(self, b):
        max_poisson = self.poisson(1, 1)
        return int(b * self.poisson(random(), 1) / max_poisson)

    def choice_poisson(self, lista):
        random = self.random_poisson(len(lista))
        return lista[random]

    def forced_instruction(self, inst):
        self.forced = True
        self.forced_isnt = inst

    def generate(self):
        self.prev_inst = copy(self.curr_isnt)
        self.curr_isnt = {'INST': '', 'OP1': '', 'OP2': ''}
        if not self.forced:
            self.curr_isnt['INST'] = self.choice_poisson(['CALC', 'WRITE', 'READ'])
            if self.curr_isnt['INST'] != 'CALC':
                self.curr_isnt['OP1'] = f'{self.random_poisson(7):3b}'.replace(' ', '0')
            if self.curr_isnt['INST'] == 'WRITE':
                self.curr_isnt['OP2'] = f'{randint(0, 65535):4X}'.replace(' ', '0')
        else:
            self.curr_isnt = copy(self.forced_isnt)
        self.forced = False
        return self.curr_isnt

    def run(self):
        while True:
            sleep(2)
            if self.steps >= 0:
                if self.steps == 0:
                    self.pause = True
                self.steps -= 1
            while self.pause and not self.next:
                pass
            self.next = False
            inst = self.generate()
            if inst['INST'] == 'READ':
                self.cache.process_cpu_read_hit(inst['OP1'])
            if inst['INST'] == 'WRITE':
                self.cache.process_cpu_write_hit(inst['OP1'], inst['OP2'])

    def view_data(self, x_offset, y_offset):
        view_strings = []
        view_curr_inst = self.curr_isnt['INST'] + ' ' + self.curr_isnt['OP1'] + ' ' + self.curr_isnt['OP2']
        view_strings.append({'x': x_offset + 255, 'y': y_offset + -31, 'string': view_curr_inst})
        view_prev_inst = self.prev_inst['INST'] + ' ' + self.prev_inst['OP1'] + ' ' + self.prev_inst['OP2']
        view_strings.append({'x': x_offset + 255, 'y': y_offset + -10, 'string': view_prev_inst})
        x = x_offset + 195
        y = y_offset + 80
        cache_blocks = self.cache.blocks
        for i in range(len(cache_blocks)):
            view_strings.append({'x': x, 'y': y + (i * 25), 'string': cache_blocks[i]['STATUS']})
            view_strings.append({'x': x + 50, 'y': y + (i * 25), 'string': cache_blocks[i]['MEMPOS']})
            view_strings.append({'x': x + 105, 'y': y + (i * 25), 'string': cache_blocks[i]['DATA']})
        return view_strings