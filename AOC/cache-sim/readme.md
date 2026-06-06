# Cache Simulator in Python

Run:

```bash
python3 main.py
```

After starting the program, a few useful commands are:

```text
load addresses/addr32.txt
stats
print
```

A cache is already created in `main.py`:

```python
    nsets=2⁶,
    blocksize_bytes=4,
    associativity=2,
    addressing=32,
    replacement="LRU"
```

`load` reads a file containing one address per line and performs a cache read for each address.

Example:

```text
load addresses/addr32.txt
```

You can also test manually:

```text
read 42
read 0x2A
read 0b101010

write 42 255
write 0x2A 0xFF
write 0b101010 0b11111111
```

Addresses and values may be provided in decimal, hexadecimal (`0x`) or binary (`0b`) notation.

Available commands:

```text
help
exit

load <file>

read <address>
write <address> <data>

stats
print
config

select
create <nsets>:<blocksize_bytes>:<associativity>:<replacement> --OPT_ADDRESSING=<8|16|32|64>
```

Example session:

```text
load addresses/addr32.txt
stats
print
```

Trace files included:

```text
addresses/addr8.txt
addresses/addr32.txt
```

Creating a new cache:
Example
```text
create 16:1:1:FIFO --OPT_ADDRESSING=8
```
Creates a cache with 16 sets, 1 byte per block, direct mapped using 'FIFO' as replacement policy and 8 bits for addressing.

Or

For a fully associative with 64 blocks, 1 byte blocks and Random replacement policy.
```text
create 1:1:64:RANDOM
```


You can view any of your created caches using
```text
select
```

And select them like
```text
select 1
```

The simulator may also be used directly from Python:

```python
from structures.cache import Cache

L1 = Cache(
    nsets=64,
    blocksize_bytes=4,
    associativity=2,
    addressing=32,
    replacement="LRU"
)

L1.read(0x2A)
L1.write(0x2A, 0xFF)

print(L1)
print(L1.getStats())
```
