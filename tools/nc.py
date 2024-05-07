import pwnlib.tubes.remote as remote
        
nc = "challenges.ulctf.ca"
port = 31337
r = remote.remote(nc,port)

def readline(endOfLine="\n"):
    data = b""
    rec = ""
    while rec != bytes(endOfLine,"utf-8"):
        rec = r.recvn(1)
        data+=rec
    return  repr(data)
    
def sendline(toSend):
    r.send(bytes(toSend,"utf-8") + b"\n")

