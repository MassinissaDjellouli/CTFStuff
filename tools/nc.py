import pwnlib.tubes.remote as remote
import math    
nc = "challenges.ringzer0ctf.com"
port = 10066
r = remote.remote(nc,port)

def readline(endOfLine="\n"):
    data = b""
    rec = ""
    while rec != bytes(endOfLine,"utf-8"):
        rec = r.recvn(1)
        data+=rec
    return repr(data)
    
def sendline(toSend):
    r.send(bytes(toSend,"utf-8") + b"\n")

yeah = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
# yeah="Tg"
moy = []
rang = 15
for i in yeah:
    x = 0
    for y in range(rang):
        readline(":")
        sendline(i)
        res = readline()
        if "Wrong" in res:
            x += float(res.split(" ")[5])
    moy.append(x/rang)
    print(i)
print(min(moy))
print(yeah[moy.index(min(moy))])
