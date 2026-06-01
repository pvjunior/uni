from structures.cache import Cache

def main():
    L1 = Cache(
        nsets=4,
        blocksize_bytes=1,
        associativity=1,
        addressing=8
    )

    L1.write(0b0000, 0xAB)
    print(L1.read(0xF))
    print(L1)

    print(L1.getStats())

    





main()
