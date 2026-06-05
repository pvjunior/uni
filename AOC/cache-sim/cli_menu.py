from pathlib import Path
from structures.cache import Cache

# This whole menu was started by me and finished by AI
class CLI_Menu:
    def __init__(self):
        self.caches = []
        self._current_cache = None

    def start(self):
        print("\033[H\033[2J", end="")
        print("Type 'help' for command list")

        while True:
            try:
                raw = input(f"\n{self.current_cache} > ")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                break

            split_command = raw.strip().split()
            self._command_handler(split_command)

    def _command_handler(self, split_command):
        if not split_command:
            return

        command = split_command[0].upper()
        params = split_command[1:]

        match command:
            case "EXIT":
                print("Exiting...")
                raise SystemExit

            case "HELP":
                self._help()

            case "LOAD":
                self._load(params)

            case "WRITE":
                self._write(params)

            case "READ":
                self._read(params)

            case "SELECT":
                self._select(params)

            case "CREATE":
                self._create(params)

            case "CONFIG":
                self._config()

            case "PRINT":
                self._print_cache()

            case "STATS":
                self._stats()

            case _:
                print("Invalid command, try again. Type 'help' for instructions")

    def pre_insert_cache(self, cache: Cache):
        self.caches.append(cache)
        self._current_cache = cache

    @property
    def current_cache(self):
        if self._current_cache is None:
            return "NO CACHE"
        return f"cache {self.caches.index(self._current_cache)}"

    @current_cache.setter
    def current_cache(self, val):
        self._current_cache = val

    def _require_cache(self):
        if self._current_cache is None:
            print("No cache selected. Use 'create' or 'select'.")
            return False
        return True

    def _parse_int(self, value: str) -> int:
        return int(value, 0)

    def _cache_summary(self, cache: Cache) -> str:
        repl = cache.replacement if cache.replacement is not None else "NONE"
        return (
            f"nsets={cache.nsets}, blocksize={cache.blocksize}B, "
            f"assoc={cache.associativity}, addr={cache.addressing}b, repl={repl}"
        )

    def _create(self, params):
        if not params:
            print("Usage:")
            print("  create <nsets>:<blocksize_bytes>:<associativity>:<replacement> --OPT_ADDRESSING=<2|4|8|16|32|64>")
            return

        spec = params[0]
        addr_bits = 32

        for p in params[1:]:
            if p.startswith("--OPT_ADDRESSING="):
                try:
                    addr_bits = int(p.split("=", 1)[1])
                except ValueError:
                    print("Invalid --OPT_ADDRESSING value")
                    return

        try:
            nsets_s, block_s, assoc_s, repl_s = spec.split(":")
            cache = Cache(
                nsets=int(nsets_s),
                blocksize_bytes=int(block_s),
                associativity=int(assoc_s),
                addressing=addr_bits,
                replacement=repl_s.upper()
            )
            self.pre_insert_cache(cache)
            print(f"Created and selected cache {self.caches.index(cache)}")
        except ValueError:
            print("Invalid create format.")
            print("Usage:")
            print("  create <nsets>:<blocksize_bytes>:<associativity>:<replacement> --OPT_ADDRESSING=<2|4|8|16|32|64>")
        except Exception as e:
            print(f"Failed to create cache: {e}")

    def _select(self, params):
        if not self.caches:
            print("No caches available.")
            return

        if not params:
            for i, cache in enumerate(self.caches):
                print(f"{i} - cache {i}: {self._cache_summary(cache)}")
            return

        try:
            idx = int(params[0])
            self.current_cache = self.caches[idx]
            print(f"Selected cache {idx}")
        except (ValueError, IndexError):
            print("Invalid cache index")



    def _stats(self):
        if not self._require_cache():
            return

        print(self._current_cache.getStats())
        
    def _config(self):
        if not self._require_cache():
            return

        c = self._current_cache
        print("CACHE CONFIG")
        print("-" * 40)
        print(f"nsets          : {c.nsets}")
        print(f"associativity   : {c.associativity}")
        print(f"blocksize bytes : {c.blocksize}")
        print(f"address bits    : {c.addressing}")
        print(f"replacement     : {c.replacement if c.replacement is not None else 'NONE'}")
        print("")
        print("ADDRESS BREAKDOWN")
        print("-" * 40)
        print(f"tag bits   : {c._tagsize}")
        print(f"index bits : {c._indexsize}")
        print(f"offset bits : {c._offset}")
        print("")
        print("BIT SPLIT")
        print("-" * 40)
        print(f"[ TAG ({c._tagsize}) | INDEX ({c._indexsize}) | OFFSET ({c._offset}) ]")

    def _print_cache(self):
        if not self._require_cache():
            return
        print(self._current_cache)

    def _read(self, params):
        if not self._require_cache():
            return
        if len(params) != 1:
            print("Usage: read <address>")
            return

        try:
            address = self._parse_int(params[0])
            before_hits = self._current_cache.stats["hit"]
            before_misses = self._current_cache.stats["miss"]

            self._current_cache.read(address)

            after_hits = self._current_cache.stats["hit"]
            after_misses = self._current_cache.stats["miss"]

            if after_hits > before_hits:
                print("HIT")
            elif after_misses > before_misses:
                print("MISS")
            else:
                print("UNKNOWN")
        except Exception as e:
            print(f"Read failed: {e}")

    def _write(self, params):
        if not self._require_cache():
            return
        if len(params) != 2:
            print("Usage: write <address> <data>")
            return

        try:
            address = self._parse_int(params[0])
            data = self._parse_int(params[1])

            before_hits = self._current_cache.stats["hit"]
            before_misses = self._current_cache.stats["miss"]

            self._current_cache.write(address, data)

            after_hits = self._current_cache.stats["hit"]
            after_misses = self._current_cache.stats["miss"]

            if after_hits > before_hits:
                print("HIT")
            elif after_misses > before_misses:
                print("MISS")
            else:
                print("UNKNOWN")
        except Exception as e:
            print(f"Write failed: {e}")

    def _load(self, params):
        if not self._require_cache():
            return
        if len(params) != 1:
            print("Usage: load <path/to/file.txt>")
            return

        path = Path(params[0])
        if not path.exists():
            print(f"File not found: {path}")
            return

        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    try:
                        self._current_cache.read(self._parse_int(line))
                    except ValueError:
                        print(f"Skipping invalid address: {line}")

            print("Load complete.")
        except Exception as e:
            print(f"Load failed: {e}")

    def _help(self):
        print("""
commands:

  help
    Shows this message.

  exit
    Exits the simulator.

cache:

  create <nsets>:<blocksize_bytes>:<associativity>:<replacement> --OPT_ADDRESSING=<2|4|8|16|32|64>
    Creates a cache and selects it.
    replacement: LRU, FIFO, RANDOM

  select
    Lists all caches.
  select <index>
    Selects a cache.

  config
    Prints current cache config, including tag/index/offset sizes.

  print
    Prints current cache state.
              
  stats
    Prints the current stats of queries, misses and hits.

usage:

  read <address>
    Reads from cache.
    Prints HIT or MISS.
    Address can be decimal, 0x hex, 0b binary, or 0o octal.

  write <address> <data>
    Writes data to cache.
    Prints HIT or MISS.
    Address and data can be decimal, 0x hex, 0b binary, or 0o octal.

  load <path/to/file.txt>
    Reads one address per line and performs a read on each.

    Example:
      0
      32
      64
      96
    Address format is the same as above.
""")