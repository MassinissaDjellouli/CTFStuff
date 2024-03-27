
def xor(key,enc):
    print(''.join([chr(x ^ key[i % len(key)]) for i,x in enumerate(enc)]))

def from_str(string:str):
    return [ord(i) for i  in string]

def xor_from_str(key:str,enc:str):
    xor(from_str(key),from_str(enc))
key = [119, 104, 52, 116, 52, 114, 51, 121, 48, 117, 100, 48, 49, 110, 103, 63]
enc = [32, 13, 88, 24, 20, 22, 92, 23, 85, 89, 68, 68, 89, 11, 71, 89, 27, 9, 83, 84, 93, 1, 57, 42, 83, 7, 13, 96, 69, 29, 86, 81, 52, 4, 7, 64, 70]

xor(key,enc)