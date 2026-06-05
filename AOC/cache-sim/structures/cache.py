from random import randbytes, randint, choice
from structures.data_block import DataBlock
from math import log

class Cache:
    def __init__(self, 
                 nsets: int,
                 blocksize_bytes: int,
                 associativity: int = 1,
                 addressing: int = 32,
                 replacement: str = "LRU"
                 ):

        if nsets % associativity and not nsets == 1:
            raise ValueError("Associativy must be ratio of nsets")

        self.nsets = nsets
        self.blocksize = blocksize_bytes
        self.associativity = associativity
        self.replacement = replacement
        self.addressing = addressing

        self.M: tuple
        self.stats = dict()

        self._initializeCache()


    def _initializeCache(self):

        cachebuild = []

        for setIndex in range(self.nsets):
            set = []
            for _ in range(self.associativity):

                block = DataBlock(
                    block_size=self.blocksize * 8,
                    tag_size=self._tagsize,
                    validator_bit=True, dirty_bit=True
                )
                set.append(block)

                if self.replacement == "LRU":
                    # I KNOW THIS IS >>>>>STUPID<<<<< but I'm not willing to create an whole system just for 3 or 4 options that will mostly just do 3 calculations and return an index
                    self.PLRU.insertInSet(setIndex, set)

            cachebuild.append(tuple(set))

        self.M = tuple(cachebuild)

        self.stats['query'] = 0
        self.stats['hit'] = 0
        self.stats['miss'] = 0


    def __str__(self):
        # AI BS
        # Determine width for the set address in binary
        width = len(bin(len(self.M) - 1)) - 1
        hexwidth = len(hex(len(self.M) - 1)) - 2



        # Build header: ADDR followed by repeating labels per associativity
        res = "    ADDR      " + "  ".join(["   TAG    DATA  VAL DIRTY  "] * self.associativity)

        # Build rows
        for addr, cache_set in enumerate(self.M):
            row = f"0x{addr:0{hexwidth}X} | {addr:0{width}b}  "
            # For each block in the set, use its __repr__
            for block in cache_set:
                row += f"{block!r}  "
            res += "\n" + row.rstrip()  # remove trailing spaces

        return res
    
    # Return true if hit, false if hit
    def check(self, address) -> bool:

        tag = address >> self.addressing - self._tagsize
        index = (address >> self._offset) & ((1 << self._indexsize) - 1)

        self.read(address)


    def read(self, address: int) -> int:
        self.stats['query'] += 1

        tag, index, offset = self._decode_address(address)

        found, block = self._fetch_block(tag, index)
        if not found:
            self.stats['miss'] += 1
            return self._refill(address)
        
        self.stats['hit'] += 1
        return block.payload

        
    def write(self, address: int, data: int):
        self.stats['query'] += 1

        tag, index, offset = self._decode_address(address)

        found, block = self._fetch_block(tag, index)
        curr_block_payload = 0x00

        if found:
            curr_block_payload = block.payload
            print(f"{curr_block_payload:b}")
            self.stats['hit'] += 1
        else:
            self.stats['miss'] += 1
        print(f"{data:b}")
        data = self._insert_byte_in_position(curr_block_payload, data, offset)
        print(f"{data:b}")
        self._write_block(address, data)
        

    def _insert_byte_in_position(self, current_block_payload: int, data_to_insert: int, offset: int) -> int:
        # That's some crazt shi
        max_offset_count = (1 << self._offset) - 1

        data_to_insert <<= 8 * (max_offset_count - offset)
        mask = 0b11111111 << 8 * (max_offset_count - offset)
        current_block_payload = (current_block_payload & ~mask)

        return (current_block_payload | data_to_insert)


    def _write_block(self, address: int, data: int, dirty: bool=True):
        tag, index, offset = self._decode_address(address)

        found, block = self._fetch_block(tag, index)
        if not found:
            set = self._fetch_set(index)
            block = self.pick_block_by_politic(set)
            
        self._update_block_data(block, tag, data)
        if not dirty:
            block.dirty = 0

    def _update_block_data(self, block: DataBlock, tag: int, data: int):

        block.tag = tag
        block.payload = data
        block.dirty = 1
        block.valid = 1

    def _refill(self, address) -> int:
        # Pretend it checks the ram....
        bytes = self._fetch_main(address)

        data = 0
        for byte in bytes:
            data = (data << 8) | byte
        # I know i could just sum(bytes). But I wanted to manipulate bytes myself as I'm not used to bitwise operations. + .sum() is generic and MAAAAYBE not as fast as joining bytes myself, but neither this code is optimized neither I'm willing to look for proof. I simply don't care enough.
        
        self._write_block(address, data, dirty=False)
        return data
    
    
    def _fetch_main(self, address) -> tuple:
        #_, index, offset = self._decode_address
        
        addressRange = (address >> self._offset) << self._offset
        bytes = bytearray()

        for byte in range(addressRange, addressRange + self._blocksize):
            bytes.append(self._get_byte_from_main(addressRange))

        return tuple(bytes)

    
    def _get_byte_from_main(self, addresss) -> int:
        # Lero lero generator
        return randbytes(1)[0] 

    
    def _decode_address(self, address) -> tuple:

        tag = address >> self.addressing - self._tagsize
        index = (address >> self._offset) & ((1 << self._indexsize) - 1)
        offset = address & self._offset

        return tag, index, offset
            
    def pick_block_by_politic(self, set: tuple) -> DataBlock:
        # TODO: add the correct strategies

        for block in set:
            if block.valid == 0:
                return block
        
        match self.replacement:
            case None:
                block = set[0]
            
            case "LRU":
                index = self.M.index(set)
                block = self.PLRU.get(index)
                print(f"tag: {block.tag:b}, payload = {block.payload:b}")

            case "FIFO":
                index = self.M.index(set)
                block = set[self.FIFO_tracking[index]]
                self.FIFO_tracking[index] = (self.FIFO_tracking[index] + 1) % self.associativity

            case "RANDOM":
                block = choice(set)

        return block

    def _fetch_set(self, index):
        return self.M[index]
    
    def _fetch_block(self, tag, index) -> tuple:
        set = self._fetch_set(index)
        for block in set:
            if (block.tag == tag) and block.valid != 0:
                return (True, block)
        
        return (False, None)
    
    @property
    def blocksize(self):
        return self._blocksize

    @blocksize.setter
    def blocksize(self, val):
        if log(val, 2) % 1:
            raise ValueError("Block size must be power of 2")
        
        self._blocksize = val
    

    def getStats(self) -> str:
        return f'''QUERIES: {self.stats['query']}\nHITS: {self.stats['hit']}\nMISSES: {self.stats['miss']}\nMISS RATIO: {(self.stats['miss']/self.stats['query'] * 100):.2f}%'''

    @property
    def nsets(self):
        return self._nsets

    @nsets.setter
    def nsets(self, val):
        if log(val, 2) % 1:
            raise ValueError("Nsets size must be power of 2")
        
        self._nsets = val

    @property
    def replacement(self):
        return self._replacement
    
    @replacement.setter
    def replacement(self, val):
        replOPTS = ["LRU", "FIFO", "RANDOM"]

        if self.associativity == 1:
            self._replacement = None
            return

        match val:
            case "LRU":
                self.PLRU = _PLRU(self.nsets, self.associativity)

            case "FIFO":
                self.FIFO_tracking = [0] * self.nsets

            case "RANDOM":
                pass

            case _:
                raise ValueError(f"{val} not an option for replacement strategy. Available options: {replOPTS}")
            
        self._replacement = val

    @property
    def addressing(self):
        return self._addressing
    
    @addressing.setter
    def addressing(self, addressing):
        addrOPTS = (2, 4, 8, 16, 32, 64)

        if not addressing in addrOPTS:
            raise ValueError(f"{addressing} bit addresses not supported, only: {addrOPTS}")
        
        self._addressing = addressing

        self._proccess_address_composition(addrOPTS)
    
    def _proccess_address_composition(self, addrOPTS):
        self._indexsize = int(log(self.nsets, 2))
        self._offset = int(log(self.blocksize, 2))
        self._tagsize = self.addressing - self._indexsize - self._offset

        if self.addressing < self._offset + self._indexsize:
            for addropt in addrOPTS:
                if addropt >= self._offset + self._indexsize:
                    suggestion = addropt
                    break
            raise ValueError(f"Incompatible addressing size with current nsets and blocksize values. nsets ({self._indexsize} bits) + blocksize ({self.blocksize_bytes} bytes, totaling {self._offset} bits for offset) is less than the available {self.addressing} bits for addressing. Addressing, for this configuration, must be {suggestion} bits or more")

class _PLRU():
    def __init__(self, nsets: int, associativity: int):
        if associativity == 1:
            raise BaseException("Associativity is 1. Something went very wrong in there pal.")
        self.sets = []

        for _ in range(nsets):
            self.sets.append([0] * (associativity - 1))
    
    def insertInSet(self, setIndex: int, ways: list):
        self.sets[setIndex].extend(ways)
    
    def get(self, setIndex: int) -> DataBlock:
        tree = self.sets[setIndex]
        
        i = 0
        while(isinstance(tree[i], int)):
            match tree[i]:
                case 0:
                    # I'm still learning how to use a binary tree as an array
                    tree[i] ^= 1
                    i = 2 * i + 1
                case 1:
                    tree[i] ^= 1
                    i = 2 * i + 2
        
        return tree[i]

    def _get_block_traversal(tree: list):
        return (tree)
        

