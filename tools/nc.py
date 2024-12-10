import pwnlib.tubes.remote as remote
import pwnlib.tubes.process as process
import time
# nc = "c.unitedctf.ca"
# port = 10033
# r = remote.remote(nc,port)
r = process.process(["/mnt/c/Users/massi/Downloads/sources-go-pwn-gown/app/gown"])

def readline(endOfLine="\n"):
    data = b""
    rec = ""
    while rec != bytes(endOfLine,"utf-8"):
        rec = r.recvn(1)
        data+=rec
    return data.decode()
def readlines(number_of_lines:int,endOfLine="\n"):
    lines = []
    for _ in range(number_of_lines):
        lines += readline(endOfLine)
    return '\n'.join(lines)
def readall():
    rec = r.recvall()
    return rec.decode()

def sendline(toSend):
    r.send(f'{toSend}\n'.encode())
def sendbytes(toSend:bytes):
    r.send(toSend)


res = readall()
print(res)
