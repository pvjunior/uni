from structures.cache import Cache

class CLI_Menu():
    def __init__(self):
        self.caches = []
        self.current_cache = None

    def start(self):
        print("\033[H\033[2J", end="")
        print("Type 'help' for getting command list")

        while(True):
            command = input(f"{self.current_cache} >  ").upper().split()
            self._command_handler(command)

    def _command_handler(self, split_command):
        if not split_command:
            return
        
        command = split_command[0]
        params = split_command[1:]

        match command:
            case "EXIT":
                print("Exiting...")
                exit()

            case "HELP":
                self._help()

            case "LOAD":
                print("Load stuff turururuuu...")

            case "WRITE":
                print("Write stuff")

            case "READ":
                print("load stuff")

            case "SELECT":
                print("select stuff")

            case "CREATE":
                print("CREATE stuff")

            case _:
                print("Invalid command, try agaiin. Type 'help' for instructions")

            

    def pre_insert_cache(self, cache: Cache):
        self.caches.append(cache)
        self.current_cache = cache

    @property
    def current_cache(self):
        if self._current_cache == None:
            return "NO CACHE"
        return f"cache {self.caches.index(self._current_cache)}"
    
    @current_cache.setter
    def current_cache(self, val):
        self._current_cache = val

    def _help(self):
        print("""
            commands:
              
                help    ---> What you're seeing now.
                exit    ---> Exits the simulator

              Cache:

                select  ---> Enters menu to select which cache you'll be working with. Options can be added using 'create'
                create  <nsets>:<blocksize_bytes>:<associativity>:<replacement> --OPT_ADDRESSING=<2|4|8|16|32|64> ---> Create cache with given config. Replacement can be 'LRU', 'FIFO' or 'RANDOM'. --OPT_ADDRESSING default is 32. 
                config  ---> prints the current cache config
            
              
              Usage:
                read <address>  ---> Reads from cache, prints 'hit' or 'miss'. Fetches data from a fake RAM.
                write <address> <data>  ---> Writes data in given address, prints hit or miss aswell.
                load <path/to/address_file.txt>     ---> Reads an file of addressings and runs 'read <address>' for each one line.
                print   ---> Prints current cache state (blocks and stuff)
""")

    