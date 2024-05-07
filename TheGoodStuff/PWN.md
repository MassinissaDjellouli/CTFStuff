[BACK](../README.md)
# PWN
## Windows stack:
- Starts at RBP
- Current at RSP
- Goes DOWN
- Return address is there

## C vulnerabilities:

    gets() <-- Reads until newline, can pass in null bytes and its gonna read them

    printf(to_print) <-- no format specifier given, we can pass our own

## Heap overflow

    Look for malloc functions
    To overflow: Number of bytes in malloc + 16 (for 64bit otherwise + 8)
    
    ex: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00cat .passwd #
        
        First 48 chars are gonna be in buffer A, the rest is gonna be in buffer B
        
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00 <- [Buffer A] cat .passwd # <- [Buffer B]

    If need to inject null byte: printf '\x00' 

If we have a shell that does not execute anything:

`(printf 'bufferoverflow' && cat) | ./program`

Adding cat at the end lets us interact with the shell.

### Use python lib pwn to do asm syscalls:

ex:
```py
    p = process("path/to/process")
    context.arch = "amd64"

    code = asm("""
    ...
    """)
    p.sendlineafter("printed text",code)
    p.interactive()
```

#### asm code ex:
![Alt text](img/asm.png)

rsp == stack pointer

Use pwn to do syscalls:
```py
        p = process("path/to/process")
        context.arch = "amd64"
        code = ""
        code += shellcraft.amd.linux.$1(arg0,...,argN)
        code += shellcraft.amd.mov(reg1,val)
        code += shellcraft.amd.linux.$2(arg0,...,argN)
        code += shellcraft.amd.linux.$3(arg0,...,argN)
        p.sendlineafter("printed text",asm(code))
```
        where $N <-- syscall name(ex: open, read, write)

### Format String vuln

- %08x prints 4 bytes of the stack in big endian format
- %016lx prints 8 bytes of the stack in big endian format
- adding n$ between the % and the format allows to offset by n
 

### Endianness:

- ELF: `readelf -h [FILE]`
- PE: Little endian
- Windows ARM: Little endian
- MIPS: Big endian but can support little endian 

### Find function offset:

#### ELF:
- Not stripped
- Func is not static or in annonymous namespace

`get_func_offset.sh [FILE] [FUNC_NAME]`

##### Function Virtual Address (VA):
`readelf -s [FILE] | grep [FUNC_NAME] | grep -o -P "[0-9a-fA-F]{16}"` 

##### .text section Offset:
`readelf -S [FILE] | grep .text | grep -o -P "[0-9a-fA-F]{8}$"`

##### .text section VA:
`objdump -h [FILE] | grep .text | grep -o -P "[0-9a-fA-F]{8}[ ]+[0-9a-f]{16}" | grep -o -P "[0-9a-fA-F]{16}"` 

Fn Offset = fn_VA - .text_VA + .text_Offset