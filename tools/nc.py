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

def readall():
    rec = r.recvall()
    return rec.decode()
def sendline(toSend):
    r.send(toSend.encode())

readline()
readline()
readline()
sendline("🗿🗿")
time.sleep(1)
sendline("__y\0")
res = readall()
print(res)
