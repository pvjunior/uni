from structures.cache import Cache

def main():
    L1 = Cache(
        nsets=8,
        blocksize_bytes=8,
        associativity=1,
        addressing=16
    )

    L1.write(0b0000, 0xAB)
    L1.read(0b0000010000101000)
    print(L1)

    print(L1.getStats())

    





main()