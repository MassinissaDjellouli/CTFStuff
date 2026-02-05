[BACK](../README.md)
# ASM
https://www.dei.isep.ipp.pt/~nsilva/ensino/ArqC/ArqC1998-1999/nguide/ng-j.htm

### ASM x86_64 jump instructions

    JA - Jump If Above
    JAE - Jump If Above or Equal
    JB - Jump If Below
    JBE - Jump If Below or Equal
    JC - Jump If Carry
    JCXZ - Jump If CX Register Zero
    JE - Jump If Equal
    JG - Jump If Greater
    JGE - Jump If Greater or Equal
    JL - Jump If Less
    JLE - Jump If Less or Equal
    JMP - Jump Unconditionally
    JNA - Jump If Not Above
    JNAE - Jump If Not Above or Equal
    JNB - Jump If Not Below
    JNBE - Jump If Not Below or Equal
    JNC - Jump If No Carry
    JNE - Jump If Not Equal
    JNG - Jump If Not Greater
    JNGE - Jump If Not Greater or Equal
    JNL - Jump If Not Less
    JNLE - Jump If Not Less or Equal
    JNO - Jump If No Overflow
    JNP - Jump If No Parity
    JNS - Jump If No Sign
    JNZ - Jump If Not Zero
    JO - Jump If Overflow
    JP - Jump If Parity
    JPE - Jump If Parity Even
    JPO - Jump If Parity Odd
    JS - Jump If Sign
    JZ - Jump If Zero

x86_64 Word length:

    word == 16 bits
    dword == double word == 32 bits
    qword == quad word == 64 bits

LEA asm instruction => Load Effective Address

    & => AND
    | => OR
    ^ => XOR
    ~ => NOT

https://stackoverflow.com/questions/43933379/what-do-the-e-and-r-prefixes-stand-for-in-the-names-of-intel-32-bit-and-64-bit-r

| 63 - 32 | 31 - 16 | 15 - 8 | 7 - 0 |
|---------|---------|--------|-------|
|         |         |   AH   |   AL  |
|         |   EAX   |   AX   |       |
|   RAX   |         |        |       |


### ASM x86_64 syscalls 
https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md

ASM x86_64 directives:

https://docs.oracle.com/cd/E26502_01/html/E28388/eoiyg.html

strace: Useful to see the syscalls that a program does.
