class DataBlock:
    def __init__(self, block_size: int,
                 tag_size: int,
                 validator_bit: bool = True,
                 dirty_bit: bool = True):
        
        self._valid = 0 if validator_bit else None
        self._dirty = 0 if dirty_bit else None
        self._tag = [0 for _ in range(tag_size)]
        self._payload = [0 for _ in range(block_size)]

        self.size = len(self._tag) + len(self._payload)
        self.size += 1 if dirty_bit else 0
        self.size += 1 if validator_bit else 0

        self._blocksize = block_size

    def __str__(self):
        res = f"{''.join(map(str, self._tag))}{''.join(map(str, self._payload))}"
        
        if self.dirty is not None:
            res = f"{self.dirty}{res}"
        
        if self.valid is not None:
            res = f"{self.valid}{res}"

        return res
    
    def __repr__(self):
        res = ""

        if self.dirty is not None:
            res = f"{res} { self.dirty} |"
        
        if self.valid is not None:
            res = f"{res} {self.valid} |"

        rawblock = self.payload
        bytes = ''
        for _ in range(int(self._blocksize / 8)):
            byte = rawblock & 0b11111111
            bytes = f"0x{byte:02X} {bytes}"
            rawblock >>= 8
        
        res = f"[ | 0x{self.tag:02X} | {bytes}|{res} ]"

        return res
    
    @property
    def tag(self):
        return int(''.join(map(str, self._tag)), 2)
    
    @tag.setter
    def tag(self, val):

        newtag = []
        tagsize = len(self._tag)

        try:
            for length, bit in enumerate(val):
                if length + 1 > tagsize:
                    raise ValueError("Tag inputed is larger than the setted size.")
                
                if not int(bit) in (0, 1):
                    raise ValueError("Tag inputed is not an array of 0's and 1's.")

                newtag.append(int(bit))
        
        except TypeError as e:
            if not str(e) == "'int' object is not iterable":
                raise BaseException(f"Well... let it explode. ----> {e}")
            
            if val >= 2**tagsize:
                ValueError(f"Tag is not an {2**tagsize} bit value.")
            newtag = [int(bit) for bit in bin(val)[2:]]

        self._tag = newtag

    @property
    def payload(self):
        return int(''.join(map(str, self._payload)), 2)
    
    @payload.setter
    def payload(self, val):

        newpayload = []
        blocksize = len(self._payload)

        try:
            for length, bit in enumerate(val):
                if length + 1 > blocksize:
                    raise ValueError("Data inputed is larger than block size.")
                
                if not int(bit) in (0, 1):
                    raise ValueError("Data inputed is not an array of 0's and 1's. neither an integer")

                newpayload.append(int(bit))
        
        except TypeError as e:
            if not str(e) == "'int' object is not iterable":
                raise BaseException(f"Well... let it explode. ----> {e}")
            
            if val >= 2**blocksize:
                ValueError(f"Data inputed is greater than {2**blocksize} bits / {blocksize / 8} bytes limit")

            newpayload = [int(bit) for bit in bin(val)[2:]]


        self._payload = newpayload

    @property
    def valid(self):
        return self._valid
    
    @valid.setter
    def valid(self, val):
        if self.valid is not None:
            self._valid = val

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, val):
        if self.dirty is not None:
            self._dirty = val

    

