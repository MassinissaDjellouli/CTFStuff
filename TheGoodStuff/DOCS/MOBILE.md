[BACK](../README.md)
# Mobile

## Android
- https://www.decompiler.com/
  - Best tool to decompile apks
- apkeasytool to extract files from apk
- apktool to decompile
  - apktool d [file.apk] -f (--force) -r (--no-res)
- to rebuild:
  - apktool b -f -r [folder] -o [output.apk] 
- Genymotion to emulate android
- APKSigner to sign
### Flutter RE

https://github.com/Impact-I/reFlutter

### Frida
#### to check out: https://frida.re

## SO files
- .so files are shared libraries
- Can be used to reverse engineer the app
- generally located in the lib folder of the apk
- Can be decompiled with binary ninja
- "native" functions in java are library functions