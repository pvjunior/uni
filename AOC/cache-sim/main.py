from structures.cache import Cache

def main():
    L1 = Cache(
        nsets=8,
        blocksize_bytes=4,
        associativity=2,
        addressing=8
    )

    L1.write(0b0000, 0xAB)
    L1.read(0b00001010)
    L1.read(0b00001010)
    print(L1)
    print("------------------------------")
    L1.write(0b00101010, 0xCC)
    print(L1)

    print(L1.getStats())

    





main()
