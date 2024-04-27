[BACK](../README.md)
# PWN
## Windows stack:
- Starts at RBP
- Current at RSP
- Goes DOWN
- Return address is there

## C vulnerabilities:

    gets() <-- Reads until newline, can pass in null bytes and its gonna read them

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
![Alt text](../image.png)

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
