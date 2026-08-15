[BACK](../README.md)
# Reverse
- DetectItEasy (die) for information about the binary
- dnSpy for dotNET and DLLs
- Ghidra/Binary ninja for all purpose
- GDB for linux
- Immunity/x64dbg for Windows
- IDA if nothing else works
  - If no idea what to find:
    - Check IDA -> Graph view for each functions
    - It is possible to draw an image using the graph view
- Strace & Ltrace
  - Library and System calls
- If code does not have main:
  - Check if it is packed
    - if contains the string "UPX":
      - use upx to unpack
      - upx -d [file] -o [output]

https://www.angusj.com/resourcehacker/

## GDB 
- info proc mappings:
  - Shows the memory mappings of the program
- info registers {reg1 reg2 ...}
  - Shows the content the specified registers
- x/{nb d'instruction}i {address}
  - prints the instructions at the specified address
- set *({address}) = {value}
  - allows to change a value at the specified memory address
- set {reg} = {value}
  - allows to change a value in a register
- set [{cast}] {addr/reg} = {value}
  - allows to cast the value to {cast} and set it
- b * {addr} 
  - adds a breakpoint at the offset
- d br
  - deletes the breakpoints
- r < {filepath} 
  - allows to run with an input file
- run < <(printf '[ToInject]')
  - allows to run with injected input into stdin
- command
  - allows to execute a command when the breakpoint is hit
  - ends with end
  - ex:
  ```
    command 1
        set $rdi = 0xdeadbeef
        echo "hello world"
        x/10x $rdi
    end
  ```
- shell
  - allows to run a shell command from gdb
- got
  - shows the Global Offset Table  
  - Also shows the protection on the GOT
- define {name}
  - Allows to define a custom function
  - ends with end
  - ex:
  - ```
    define save_registers
        shell python run.py
        info proc mappings
        run
    end
  ```
- vmmap {address}
  - shows the memory mapping of the address
  - $rip can be used as address to get the current instruction mapping
- ptype {struct}
  - shows the definition of a struct 
## Python
https://github.com/zrax/pycdc
https://pyinstxtractor-web.netlify.app/
https://pylingual.io/

## Arduino 
### ATMega328
https://www.jonaslieb.de/blog/arduino-ghidra-intro/
- RESET interrupt handler
- 2 functions in the bottom, first is the main function
  - Main is split in the setup and loop functions
  - loop is in the `do {...} while(true);`

## C#/DotNET
- dnSpy
- if the file seems obfuscated: de4dot
  - de4dot -d [file]
    - detect the obfuscator
  - de4dot -r [directory] -ru -ro [output_directory]
    - recursively deobfuscate all the files in a directory

## Baremetal
### Reset Vector
- The reset vector are the very first instructions that are executed when the system boots

### Entry Point
- The entry point can be found from the Reset vector
  - Either the start call is [ResetVector] -> [C Runtime] -> [main] or directly [C Runtime] -> [main]
    - Basically use the C Runtime as the Reset Vector
  - At the start of the program, the stack pointer is initialized
  - If we find a function that sets the stack pointer to a high address, that is likely the entry point

### Flattened Device Tree (FDT)
- Used in embedded systems to describe the hardware/peripherals
- Usually passed to the kernel at boot time
- We can use QEMU to dump the FDT and the device-tree-compiler package to decompile it
  - sudo apt install device-tree-compiler
  - qemu-system-[ARCH] -machine [MACHINE],dumpdtb [FILE.dtb] -nographic
  - dtc -I dtb -O dts FDT.dtb > out.dts

### QEMU
- -kernel option:
  - Load a ELF in memory and jump to the entry point
- -device option:
  - Allows to load an executable or raw binary
  - Allows to set the instruction pointer to a specific address
  - if we want to run raw binary, add force-raw=on
- -bios option:
  - opensbi can cause problems with some firmwares
  - use -bios none to disable it
### GDB
- we can use -s to expose GDB on port 1234 and -S to wait for GDB connection before starting the CPU
- gdb-multiarch for cross architecture debugging 
- set architecture [ARCH] in GDB to set the architecture
- target extended-remote 127.0.0.1:1234 to connect to QEMU

## Java
### Tools
- Bytecode-viewer
  - Pretty useful to use different decompilers/dissasemblers on the same program
- Krakatau
  - Pretty much the best dissasembler/assembler for Java bytecode 
### Bytecode
- Differents variants of instructions depending on the size of the values:
  - int/floats/fct_ref -> 1 slot
  - longs/doubles -> 2 slots
- ldc/ldc2_w
  - loads a constant in the stack

## Windows 16-bit / DOS
- VDOS
  - the DEBUG software comes with it
  - Works like a simplified version of GDB
- https://wiki.osdev.org/Expanded_Main_Page
  - Contains loads of info on old disk images/old os reverse
### Floppy images
- If its a DOS/MBR bootsector: offset is usually 0x7C00 in binja
- qemu-system-x86_64 -drive format=raw,file=[FILE]

## WASM

- HELL
- wabt is very useful to convert between wat and wasm
  - wasm2c is very useful to convert wasm to c code
    - wasm2c [FILE.wasm] -o [FILE.c]
    - gcc -c -o wasmbin [WASM.C] -I wabt/wasm2c
      - wabt/wasm2c is from the source code repository of wabt
      - needed to have the headers
  - Makes it much easier to understand the code
  - Gives the function names 
  - wasm2wat will also give the function names in the wat format
### How it works
- Stack based virtual machine
- Each function has its own local variables and parameters
- The instructions operate on the values on the stack
- get instructions will push a value to the stack, set instructions will pop a value from the stack and store it in a local variable or memory
- load instructions will load a value from memory and push it to the stack, store instructions will pop a value from the stack and store it in memory
- The memory is a linear array of bytes, the stack is also a linear array of values
- The instructions act on the values on the stack, for example:
  - i32.add will pop 2 values from the stack, add them and push the result to the stack
- global variables are available to all functions and can be accessed using get_global and set_global instructions
  - They are also available in js
- 
### Instructions
- i[xx]_load[yy]_[s/u]
  - xx = i32/i64/f32/f64
  - yy = 8/16/32 
  - loads a value of yy bits and sign extends it to xx bits
  - s is for signed, u is for unsigned
  - ex:
    - i32_load16_s will load 16 bits from memory, sign extend it to 32 bits and push it to the stack
- i[xx]_store[yy]
  - xx = i32/i64/f32/f64
  - yy = 8/16/32
  - pops a value from the stack and stores it in memory as yy bits
  - ex:
  -   - i32_store16 will pop a value from the stack and store it in memory as 16 bits
- i[xx]_[op]
  - op = add/sub/mul/div/srem/urem/and/or/xor
  - pops 2 values from the stack, performs the operation and pushes the result to the stack
  - ex:
    - i32_add will pop 2 values from the stack, add them and push the result to the stack
- i[xx].const [value]
  - pushes a constant value to the stack
- import [module] [name] (func [wasm_name] (param [type1] [type2] ...) (result [type]))
  - imports a function from js/the host environment
  - the function can then be called from the wasm code

## Radare2
- rabin2 -I [binary]
  - Shows important info about the binary, including the architecture and compiler used.

## Patterns
- AES:
  - Lots of xor operations, operations on blocks of 16 (usually in blocks of 4x4 bytes):
  - To figure out if it is encryption or decryption, we can try to find the SBox lookup table and figure out if it is the regular SBox or the inverse SBox.
  - Sbox is a substitution box used in AES encryption. So in the decompiled code it might look like this:
    ```c
    //In each case, "some_memory_address" is the address of the SBox lookup table. It should contains a certain set of bytes.
    bytes_to_encrypt[idx] = some_memory_address + bytes_to_encrypt[idx]
    //or
    for (int idx = 0; idx < 16; idx++) {
      bytes_to_encrypt + idx = some_memory_address + bytes_to_encrypt + idx
    }
    //or
    for (int idx = 0; idx < 4; idx++) {
      int* x1 = bytes_to_encrypt + idx << 2
      int* x2 = bytes_to_encrypt + (idx + 1) << 2
      int* x3 = bytes_to_encrypt + (idx + 2) << 2
      int* x4 = bytes_to_encrypt + (idx + 3) << 2

      *x1 + idx << 2 = some_memory_address + *x1 + idx << 2
      *x2 + idx << 2 = some_memory_address + *x2 + idx << 2
      *x3 + idx << 2 = some_memory_address + *x3 + idx << 2
      *x4 + idx << 2 = some_memory_address + *x4 + idx << 2
    }  
    ```
    - Regular sbox lookup table starts with these bytes: `0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5`
    - Inverse sbox lookup table starts with these bytes: `0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38`
- Linked List:
  - Insert
    - Either recursive or iterative
      - If recursive, the function will call itself with the next node pointer as an argument
        - Something like `insert(node_ptr, value) = IF (*node_ptr[0] == null) -> *node_ptr[1] = value ELSE insert(*node_ptr[0],value)`
      - If iterative, the function will have a loop that traverses the list until it finds the right place to insert the new node
        - Something like `insert(node_ptr, value) = WHILE (*node_ptr[0] != null) -> node_ptr = *node_ptr[0] ELSE *node_ptr[1] = value `
    - Decompiled example (recursive):
    ```c
      int64_t push_val_to_linked_list(int64_t* arg1, int32_t arg2)
      {
        if (!arg1)
            return 0;
        
        int64_t* var_20_1;
        
        if (*(uint64_t*)arg1)
        {
            int64_t rax_8 = *(uint64_t*)arg1;
            **(uint64_t**)arg1 = push_val_to_linked_list(rax_8, (uint64_t)arg2, rax_8);
            var_20_1 = *(uint64_t*)arg1;
        }
        else
        {
            var_20_1 = malloc(0x10);
            
            if (!var_20_1)
            {
                exit(0);
                /* no return */
            }
            
            var_20_1[1] = arg2;
            *(uint64_t*)var_20_1 = *(uint64_t*)arg1;
        }
        
        *(uint64_t*)arg1 = var_20_1;
        return *(uint64_t*)arg1;
      }
    ```
    - In the insert we might see a malloc for the new node to be added. otherwise, the malloc will be called outside and the pointer to the new node will be passed as an argument to the insert function.
    - So when looking for xrefs using malloc, we can find this pattern close to the malloc call.
    - The same logic can be applied to free for the node removal functions
  - Removal:
    - Dissasembled example:
    ```c
      int64_t sub_400c33(int64_t* arg1, int32_t arg2)
      {
          int64_t* var_20 = arg1;
          int64_t result;
          
          while (true)
          {
              result = *(uint64_t*)var_20;
              
              if (!result)
                  break;
              
              int64_t* rax_2 = *(uint64_t*)var_20;
              
              if (arg2 != *(uint32_t*)(*(uint64_t*)var_20 + 8))
                  var_20 = *(uint64_t*)var_20;
              else
              {
                  *(uint64_t*)var_20 = **(uint64_t**)var_20;
                  rax_2[1] = 0;
                  *(uint64_t*)rax_2 = 0;
                  free(rax_2);
                  int64_t var_10_2 = 0;
              }
          }
          
          return result;
      }
    ```
- Direct threaded code:
  - Instead of having a central loop, we jump from one address to another
  - So a function will execute some instructions, then jump to another function, which will execute some instructions, then jump to another function, and so on.
  - Can be either using a list of function pointers or computing the next function address
  - We will see a lot of `jmp rax(or any register)` or `call rax(or any register)` instructions
  - Makes it harder to follow the control flow if it is calculated at runtime since we will need to dynamically compute the next function address to know where the control flow will go next
- PCG32 PRNG:
  - `0x14057b7ef767814f` is the increment and `0x5851f42d4c957f2d` is the multiplier
- SplitMix64
  - Follows the following formula:
    - x = Seed; x ^= (x >> 30); x *= 0xbf58476d1ce4e5b9; x ^= (x >> 27); x *= 0x94d049bb133111eb; x ^= (x >> 31);Seed++
      - x >> 30 -> x >> 0x1e
      - x >> 27 -> x >> 0x1b
      - x >> 31 -> x >> 0x1f
      - 0xbf58476d1ce4e5b9 -> -0x40a7b892e31b1a47
      - 0x94d049bb133111eb -> -0x6b2f9e44ecceee15
  - It's a PRNG
  - Reversible
- VMs:
  - Struct with these fields:
    - IP
    - Memory pointer (or memory block)
    - Pointer to the instructions
  - Big memory allocation
    - Usually for the VM memory
    - Can be on the stack or on the heap using malloc
    - If on the stack, we will see a big stack frame
      - Something like `sub rsp, 0x1000` or `sub rsp, 0x2000` or even bigger
  - The VM memory is usually a big array of bytes, so we will see a lot of `mov [reg+offset], reg` or `mov reg, [reg+offset]` instructions
  - VM Dispatch:
    - Either a big switch statement or a jump table
    - From the Instruction pointer we decode it and use it as the switch case or the jump table index

# Python RE Helper Functions (Shallout P.S.Y <3)
> Mimicking C primitives for reverse engineering work

---

## Bit Rotation

```python
def rotl8(v, n):  return ((v << n) | (v >> (8  - n))) & 0xFF
def rotr8(v, n):  return ((v >> n) | (v << (8  - n))) & 0xFF

def rotl16(v, n): return ((v << n) | (v >> (16 - n))) & 0xFFFF
def rotr16(v, n): return ((v >> n) | (v << (16 - n))) & 0xFFFF

def rotl32(v, n): return ((v << n) | (v >> (32 - n))) & 0xFFFFFFFF
def rotr32(v, n): return ((v >> n) | (v << (32 - n))) & 0xFFFFFFFF

def rotl64(v, n): return ((v << n) | (v >> (64 - n))) & 0xFFFFFFFFFFFFFFFF
def rotr64(v, n): return ((v >> n) | (v << (64 - n))) & 0xFFFFFFFFFFFFFFFF
```

```python
# Usage
rotl8(0x41, 3)    # → 0x0A
rotr8(0x0A, 3)    # → 0x41  (inverse)
rotl32(0xDEADBEEF, 16)  # → 0xBEEFDEAD
```

> Python integers are arbitrary precision — always mask with `& 0xFF` etc.
> after shifts or you get values that silently exceed the intended bit width.

---

## Arithmetic Helpers

```python
# Unsigned addition with overflow (mimics C uint behaviour)
def add8(a, b):   return (a + b) & 0xFF
def add16(a, b):  return (a + b) & 0xFFFF
def add32(a, b):  return (a + b) & 0xFFFFFFFF
def add64(a, b):  return (a + b) & 0xFFFFFFFFFFFFFFFF

# Unsigned subtraction with underflow
def sub8(a, b):   return (a - b) & 0xFF
def sub16(a, b):  return (a - b) & 0xFFFF
def sub32(a, b):  return (a - b) & 0xFFFFFFFF
def sub64(a, b):  return (a - b) & 0xFFFFFFFFFFFFFFFF

# Unsigned multiplication with truncation
def mul8(a, b):   return (a * b) & 0xFF
def mul16(a, b):  return (a * b) & 0xFFFF
def mul32(a, b):  return (a * b) & 0xFFFFFFFF
def mul64(a, b):  return (a * b) & 0xFFFFFFFFFFFFFFFF
```

```python
# Usage
add8(0xF0, 0x20)   # → 0x10  (wraps, same as C uint8_t)
sub8(0x10, 0x20)   # → 0xF0  (underflow, same as C uint8_t)
```

---

## Signed / Unsigned Conversion

```python
# Reinterpret an unsigned value as signed (mimics C casting)
def to_signed8(v):  return v - 0x100        if v & 0x80   else v
def to_signed16(v): return v - 0x10000      if v & 0x8000 else v
def to_signed32(v): return v - 0x100000000  if v & 0x80000000 else v

# Reinterpret a signed value as unsigned
def to_unsigned8(v):  return v & 0xFF
def to_unsigned16(v): return v & 0xFFFF
def to_unsigned32(v): return v & 0xFFFFFFFF
```

```python
# Usage
to_signed8(0xFF)    # → -1
to_signed8(0x7F)    # → 127
to_signed32(0xFFFFFFFF)  # → -1
```

---

## Byte Swapping (Endianness)

```python
def bswap16(v): return ((v & 0xFF) << 8) | ((v >> 8) & 0xFF)

def bswap32(v):
    return (((v & 0x000000FF) << 24) |
            ((v & 0x0000FF00) <<  8) |
            ((v & 0x00FF0000) >>  8) |
            ((v & 0xFF000000) >> 24))

def bswap64(v):
    return (((v & 0x00000000000000FF) << 56) |
            ((v & 0x000000000000FF00) << 40) |
            ((v & 0x0000000000FF0000) << 24) |
            ((v & 0x00000000FF000000) <<  8) |
            ((v & 0x000000FF00000000) >>  8) |
            ((v & 0x0000FF0000000000) >> 24) |
            ((v & 0x00FF000000000000) >> 40) |
            ((v & 0xFF00000000000000) >> 56))
```

```python
# Or just use struct (simpler for buffers)
import struct

def bswap32_buf(data):
    return struct.pack('>I', struct.unpack('<I', data)[0])

# Usage
bswap32(0xDEADBEEF)   # → 0xEFBEADDE
```

---

## Packing / Unpacking (struct shortcuts)

```python
import struct

# Single values
def p8(v):    return struct.pack('B', v & 0xFF)
def p16le(v): return struct.pack('<H', v & 0xFFFF)
def p16be(v): return struct.pack('>H', v & 0xFFFF)
def p32le(v): return struct.pack('<I', v & 0xFFFFFFFF)
def p32be(v): return struct.pack('>I', v & 0xFFFFFFFF)
def p64le(v): return struct.pack('<Q', v & 0xFFFFFFFFFFFFFFFF)
def p64be(v): return struct.pack('>Q', v & 0xFFFFFFFFFFFFFFFF)

def u8(b):    return struct.unpack('B',  b[:1])[0]
def u16le(b): return struct.unpack('<H', b[:2])[0]
def u16be(b): return struct.unpack('>H', b[:2])[0]
def u32le(b): return struct.unpack('<I', b[:4])[0]
def u32be(b): return struct.unpack('>I', b[:4])[0]
def u64le(b): return struct.unpack('<Q', b[:8])[0]
def u64be(b): return struct.unpack('>Q', b[:8])[0]
```

```python
# Usage
p32le(0xDEADBEEF)          # → b'\xef\xbe\xad\xde'
u32le(b'\xef\xbe\xad\xde') # → 0xDEADBEEF
```

---

## XOR Helpers

```python
# XOR two byte strings (truncates to shortest)
def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# XOR a buffer with a repeating key
def xor_key(buf, key):
    key = key if isinstance(key, (bytes, bytearray)) else bytes([key])
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(buf))

# XOR with previous byte (CBC-like decode, right to left)
def xor_chain_decode(buf, iv=0x00):
    buf = bytearray(buf)
    for i in range(len(buf) - 1, 0, -1):
        buf[i] ^= buf[i - 1]
    buf[0] ^= iv
    return bytes(buf)
```

```python
# Usage
xor(b'\xDE\xAD', b'\xFF\xFF')          # → b'!R'
xor_key(b'hello', 0x42)                # → repeating single-byte key
xor_key(b'hello world', b'\xAA\xBB')  # → repeating multi-byte key
```

---

## Bit Manipulation

```python
# Extract a bitfield: bits [hi:lo] from value (inclusive, like C bitfields)
def bits(v, hi, lo):
    mask = (1 << (hi - lo + 1)) - 1
    return (v >> lo) & mask

# Test a single bit
def bit(v, n): return (v >> n) & 1

# Set / clear / toggle a bit
def set_bit(v, n):    return v | (1 << n)
def clear_bit(v, n):  return v & ~(1 << n)
def toggle_bit(v, n): return v ^ (1 << n)

# Population count (number of 1 bits) — mimics __builtin_popcount
def popcount(v): return bin(v).count('1')

# Count leading zeros (mimics __builtin_clz, 32-bit)
def clz32(v):
    if v == 0: return 32
    return 31 - int(v).bit_length() + 1
```

```python
# Usage
bits(0b11011010, 5, 3)   # → 0b011 = 3  (bits 5 down to 3)
bit(0xAB, 3)             # → 1
popcount(0xFF)           # → 8
clz32(0x00000001)        # → 31
```

---

## S-box Helpers

```python
import numpy as np

# Build inverse S-box from a forward S-box (must be a bijection)
def inv_sbox(sbox):
    table = [0] * 256
    for i, v in enumerate(sbox):
        table[v] = i
    return table

# numpy version (faster for large buffers)
def inv_sbox_np(sbox):
    return np.argsort(np.array(sbox, dtype=np.uint8)).astype(np.uint8)

# Apply S-box substitution to a buffer
def apply_sbox(buf, table):
    return bytes(table[b] for b in buf)

# Check if a table is a valid bijection (required for invertibility)
def is_bijection(table):
    return len(set(table)) == 256 and len(table) == 256
```

```python
# Usage
sbox = list(range(256))   # identity sbox (trivial example)
inv  = inv_sbox(sbox)
assert apply_sbox(b'hello', sbox) == b'hello'
assert is_bijection(sbox)
```

---

## Modular Inverse

```python
# Built-in (Python 3.8+) — raises ValueError if inverse doesn't exist
def mod_inv(k, mod):
    return pow(k, -1, mod)

# Brute-force fallback for small moduli
def mod_inv_brute(k, mod):
    for i in range(1, mod):
        if (k * i) % mod == 1:
            return i
    return None   # no inverse exists (k shares a factor with mod)
```

```python
# Usage — encoder does v = (v * 0x35) % 256
inv_k = mod_inv(0x35, 256)          # → 101
assert (0x35 * inv_k) % 256 == 1

# Decoder
def decode_byte(v): return (v * inv_k) % 256
```

---

## Useful One-Liners

```python
# Hex dump a buffer
def hexdump(buf, width=16):
    for i in range(0, len(buf), width):
        chunk = buf[i:i+width]
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        asc_part = ''.join(chr(b) if 0x20 <= b < 0x7F else '.' for b in chunk)
        print(f'{i:08x}  {hex_part:<{width*3}}  {asc_part}')

# Convert hex string to bytes
def h(s): return bytes.fromhex(s.replace(' ', ''))

# Print a value in all common representations
def inspect(v, bits=32):
    mask = (1 << bits) - 1
    v &= mask
    print(f'hex: {v:#0{bits//4+2}x}')
    print(f'dec: {v}')
    print(f'bin: {v:0{bits}b}')
    print(f'signed: {to_signed32(v) if bits == 32 else v}')
```

```python
# Usage
hexdump(b'\xDE\xAD\xBE\xEF' * 4)
h('DE AD BE EF')   # → b'\xde\xad\xbe\xef'
inspect(0xDEADBEEF)
```

---

## SplitMix64

```python
VALUE = 0x0000000000000000  # the output you want to invert
GOLD  = 0x9E3779B97F4A7C15  # added constant (varies per implementation)
A     = 0xBF58476D1CE4E5B9  # first multiplier
B     = 0x94D049BB133111EB  # second multiplier
S1    = 30                  # first shift
S2    = 27                  # second shift
S3    = 31                  # final shift
M = (1 << 64) - 1
A_INV = pow(A, -1, 1 << 64)
B_INV = pow(B, -1, 1 << 64)

def unxor(y, s):
    x = y
    for _ in range(64 // s + 1):
        x = y ^ (x >> s)
    return x

def mix(x):
    x = (x + GOLD) & M
    x = ((x ^ (x >> S1)) * A) & M
    x = ((x ^ (x >> S2)) * B) & M
    return x ^ (x >> S3)

def unmix(z):
    z = unxor(z & M, S3)
    z = (z * B_INV) & M
    z = unxor(z, S2)
    z = (z * A_INV) & M
    z = unxor(z, S1)
    return (z - GOLD) & M

x = unmix(VALUE)
print(x)
print(hex(x))
print("ok" if mix(x) == (VALUE & M) else "FAILED")
```

## All-in-one Import Block

Copy this at the top of any RE script to have everything available:

```python
import struct, numpy as np
from sympy import mod_inverse

# --- rotations ---
def rotl8(v,n):  return ((v<<n)|(v>>(8-n)))  &0xFF
def rotr8(v,n):  return ((v>>n)|(v<<(8-n)))  &0xFF
def rotl32(v,n): return ((v<<n)|(v>>(32-n))) &0xFFFFFFFF
def rotr32(v,n): return ((v>>n)|(v<<(32-n))) &0xFFFFFFFF

# --- arithmetic ---
def add8(a,b):  return (a+b)&0xFF
def sub8(a,b):  return (a-b)&0xFF
def mul8(a,b):  return (a*b)&0xFF
def add32(a,b): return (a+b)&0xFFFFFFFF
def sub32(a,b): return (a-b)&0xFFFFFFFF
def mul32(a,b): return (a*b)&0xFFFFFFFF

# --- sign ---
def to_signed8(v):  return v-0x100       if v&0x80       else v
def to_signed32(v): return v-0x100000000 if v&0x80000000 else v

# --- pack/unpack ---
def p32le(v): return struct.pack('<I', v&0xFFFFFFFF)
def u32le(b): return struct.unpack('<I', b[:4])[0]
def p64le(v): return struct.pack('<Q', v&0xFFFFFFFFFFFFFFFF)
def u64le(b): return struct.unpack('<Q', b[:8])[0]

# --- xor ---
def xor(a,b):     return bytes(x^y for x,y in zip(a,b))
def xor_key(buf,key):
    key = key if isinstance(key,(bytes,bytearray)) else bytes([key])
    return bytes(b^key[i%len(key)] for i,b in enumerate(buf))

# --- sbox ---
def inv_sbox(sbox): t=[0]*256; [t.__setitem__(v,i) for i,v in enumerate(sbox)]; return t
def apply_sbox(buf,t): return bytes(t[b] for b in buf)

# --- misc ---
def bits(v,hi,lo): return (v>>lo)&((1<<(hi-lo+1))-1)
def mod_inv(k,mod): return pow(k,-1,mod)
def h(s): return bytes.fromhex(s.replace(' ',''))
def hexdump(buf,w=16):
    for i in range(0,len(buf),w):
        c=buf[i:i+w]
        print(f'{i:08x}  {" ".join(f"{b:02x}" for b in c):<{w*3}}  {"".join(chr(b) if 0x20<=b<0x7F else "." for b in c)}')
```