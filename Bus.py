class Bus:
    def __init__(self, memory):
        self.caches = []
        self.memory = memory

    def connecting(self, cache):
        self.caches.append(cache)

    def invalidate(self, cache_id, memPos):
        total = len(self.caches)
        for i in range(0, total):
            n = (cache_id + (i + 1)) % total
            self.caches[n].set_block_status(memPos, 'I')

    def readMiss(self, cache_id, memPos):
        self.memory.wait()
        total = len(self.caches)
        for i in range(0, total):
            n = (cache_id + (i + 1)) % total
            shared_data = self.caches[n].process_bus_read_miss(memPos)
            print("Read miss en ", memPos, "\n")
            if shared_data:
                return {'SHARED': True, 'DATA': shared_data}
        memData = self.memory.read_block(memPos)
        return {'SHARED': False, 'DATA': memData}

    def writeMiss(self, cache_id, memPos):
        total = len(self.caches)
        for i in range(0, total):
            n = (cache_id + (i + 1)) % total
            self.caches[n].process_bus_write_miss(memPos)
            print("Write miss en ", memPos, "\n")

    def writeThrough(self, memPos, data):
        self.memory.wait()
        self.memory.write_block(memPos, data)