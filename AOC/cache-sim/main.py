from structures.cache import Cache

def main():
    L1 = Cache(
        nsets=8,
        blocksize_bytes=4,
        associativity=1,
        addressing=8,
        replacement="RANDOM"
    )

    L1.write(0b0000, 0xAB)
    L1.read(0b00101010)
    L1.read(0b00101010)
    print(L1)
    print("------------------------------")
    L1.write(0b00101010, 0xCC)
    print(L1)
    L1.write(0b01101010, 0xFF)
    print(L1)
    L1.write(0b11101010, 0xEE)
    print(L1)
    L1.write(0b11001010, 0xDD)
    print(L1)


    print(L1.getStats())

    





main()
