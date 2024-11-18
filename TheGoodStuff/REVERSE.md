[BACK](../README.md)
# Reverse

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