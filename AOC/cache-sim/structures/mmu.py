from structures.cache import Cache
# UHHHHHHHHHHHHHHHHHHHHH
class MMU:
    def __init__(self,
                  cacheL1: Cache = None, 
                  cacheL2: Cache = None, 
                  cacheL3: Cache = None,
                  main=None,
                  auxiliary=None):
        
        self.cacheL1 = cacheL1
        self.cacheL2 = cacheL2
        self.cacheL3 = cacheL3
        self.main = main
        self.auxiliary = auxiliary

        self.cache = [self.cacheL1, self.cacheL2, self.cacheL3]

    def append(self, memoryunit):

        if memoryunit.isinstance(Cache):
            for cache in self.cache:
                if cache is None:
                    cache = memoryunit
                    return
                
        # TODO: other memory
    
    def get(self, address):

        
        block = self.cacheL1.read(address)
        self.cacheL1.stats['query'] += 1
        

        if ~(block.tag ^ (address >> (self.cacheL1._offset + self.cacheL1._indexsize))):
            self.cacheL1.stats['hit'] += 1
            
        else:
            self.cacheL1.write(address, 0x00)
            self.cacheL1.stats['miss'] += 1

        