from structures.cache import Cache
from cli_menu import CLI_Menu

def main():
    L1 = Cache(
        nsets=(2**6),
        blocksize_bytes=4,
        associativity=2,
        addressing=32,
        replacement="LRU"
    )

    menu = CLI_Menu()
    menu.pre_insert_cache(L1)

    menu.start()


    





main()
