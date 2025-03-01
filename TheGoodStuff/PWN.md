[BACK](../README.md)
# PWN
## Numbers:
- Try negative number
- Try int overflow: 4294967295
- Try long overflow: 18446744073709551615
- Try 0
- Try decimal numbers
## Windows stack:
- Starts at RBP
- Current at RSP
- Goes DOWN
- Return address is there
## Checklist
- file [path]
    - 64 or 32 bit
    - x86_64, Arm, x86?
- checksec
    - check securities on the file

## ELF files
PLT: Procedure linkage table
- Useful for dynamically linked files
- 
### Checksec

RELRO:
- Read Only Relocation
- Moves
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
![Alt text](img/syscalls.png)

https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md
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

Use pwnlib to do syscalls:
```py
        from pwnlib.shellcraft import amd64
        from pwnlib.asm import asm
        p = process("path/to/process")
        context.arch = "amd64"
        code = ""
        code += shellcraft.amd64.linux.$1(arg0,...,argN)
        code += shellcraft.amd64.mov(reg1,val)
        code += shellcraft.amd64.linux.$2(arg0,...,argN)
        code += shellcraft.amd64.linux.$3(arg0,...,argN)
        p.sendlineafter("printed text",asm(code,arch="amd64"))
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

## Shellcode optimisations (amd64):
- Use xor regA,regA -> set 0 
- push 0; pop regA -> same length as xor
- Use xchg to swap registers instead of 2 mov
- push regA pop regB -> less bytes than a mov
- xor regA,regA ; inc regA -> set 1
- Using lower registers (ex: rax -> eax -> al) will give a different bytecode

### Registers prefixes
##### Extended regs(rax):
48 
##### 32 bit regs(eax):
none
##### 16 bit regs(ax)
66
##### 8 bit regs(al/ah)
[decrement op num] 

### Assembly to byte:

xor: [reg prefix] 31 [registers]

mov: [reg prefix] 89 [registers]

### registers:

    (rax,eax,ax):
    al: 0xD8
    ah: 0xDC

    (rdi,edi,di):
    dil: 0xDF
    dih: 0xDE

    (rdx,edx,dx):
    dl: 0xDA
    dh: 0xDF

    (rsi,esi,si):
    sl: 0xDE 
    (no sih)

## ROP:
- Find gadgets:
  - objdump
  - `rp++ --unique -r [gadget_length] -f [file]`
    - length 2 should be good
- Can jump in middle of instruction
- Jumping to leave will move rbp to rbp
- Try building shellcode of what is needed then try to recreate it with gadgets
  - Syscalls are very rare
- 