[BACK](../README.md)
# Reverse

- DetectItEasy (die) for information about the binary
- dnSpy for dotNET and DLLs
- Ghidra/Binary ninja for all purpose
- GDB for linux
- Immunity/x64dbg for Windows
- IDA if nothing else works

    If no idea what to find:

    Check IDA -> Graph view for each functions
    It is possible to draw an image using the graph view

- Strace & Ltrace
  - Library and System calls

- If code does not have main:
  - Check if it is packed
    - if contains the string "UPX":
      - use upx to unpack
      - upx -d [file] -o [output]

https://www.angusj.com/resourcehacker/

## Python
https://github.com/zrax/pycdc
https://pyinstxtractor-web.netlify.app/
https://pylingual.io/

## Arduino 
### ATMega328
https://www.jonaslieb.de/blog/arduino-ghidra-intro/
- RESET interrupt handler
- 2 functions in the bottom, first is the main function
  - Main is split in the setup and loop functions
  - loop is in the `do {...} while(true);`

## C#/DotNET
- dnSpy
- if the file seems obfuscated: de4dot
  - de4dot -d [file]
    - detect the obfuscator
  - de4dot -r [directory] -ru -ro [output_directory]
    - recursively deobfuscate all the files in a directory