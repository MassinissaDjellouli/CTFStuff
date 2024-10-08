import pwnlib.tubes.remote as remote
import time
nc = "c.unitedctf.ca"
port = 10033
r = remote.remote(nc,port)

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

print(readlines(3))
sendline("🗿🗿")
time.sleep(1)
sendline("__y\0")
res = readall()
print(res)
