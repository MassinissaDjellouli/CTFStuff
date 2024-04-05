
def xor(key,enc):
    print(''.join([chr(x ^ key[i % len(key)]) for i,x in enumerate(enc)]))

def from_str(string:str):
    return [ord(i) for i  in string]

def xor_from_str(key:str,enc:str):
    xor(from_str(key),from_str(enc))


enc = [59,101,33,10,56,0,54,29,10,61,97,39,17,102,39,10,33,29,97,59,10,45,101,39,10,102,54,48,103,108,100,108]
key = [0x55]
xor(key,enc)