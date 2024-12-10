[BACK](../README.md)
# Crypto
## Hashcat

Password bruteforce cracking from a hash: Hashcat

    hashcat -a 0(brute force) -m [n] (n = hash type) file.hash rockyou.txt
    hashcat -a 0(brute force) -m [n] (n = hash type) file.hash rockyou.txt -r oneruletorulethemall.rule

To determine hash type: Check the begining of the hash:

- $2y <- BCRYPT (uncrackable)
- $2a <- BCRYPT (crackable)
## RSA

https://github.com/RsaCtfTool/RsaCtfTool

    RsaCtfTool.py --decrypt CIPHERTEXT -n N -e E

```python
from Crypto.Util.number import inverse
from Crypto.PublicKey import RSA

key = RSA.importKey(asciikey)
n = int(key.n)
e = int(key.e)
```

## Zip passwords
```bash 
zip2john [ZIP] > out
john --format=PKZIP --wordlist=/share/wordlists/rockyou.txt out
```

## mRemoteNg config files
- https://www.errno.fr/mRemoteNG
- Default pwd: `mR3m`
- `python3 tools/mremoteng_decrypt.py [FILE]` to decrypt the passwords