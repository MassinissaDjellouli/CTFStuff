[BACK](../README.md)
# Reverse
- DetectItEasy (die) for information about the binary
- dnSpy for dotNET and DLLs
- Ghidra/Binary ninja for all purpose
- GDB for linux
- Immunity/x64dbg for Windows
- IDA if nothing else works
  - If no idea what to find:
    - Check IDA -> Graph view for each functions
    - It is possible to draw an image using the graph view
- Strace & Ltrace
  - Library and System calls
- If code does not have main:
  - Check if it is packed
    - if contains the string "UPX":
      - use upx to unpack
      - upx -d [file] -o [output]

https://www.angusj.com/resourcehacker/

## GDB 
- info proc mappings:
  - Shows the memory mappings of the program
- info registers {reg1 reg2 ...}
  - Shows the content the specified registers
- x/{nb d'instruction}i {address}
  - prints the instructions at the specified address
- set *({address}) = {value}
  - allows to change a value at the specified memory address
- set {reg} = {value}
  - allows to change a value in a register
- set [{cast}] {addr/reg} = {value}
  - allows to cast the value to {cast} and set it
- b * {addr} 
  - adds a breakpoint at the offset
- d br
  - deletes the breakpoints
- r < {filepath} 
  - allows to run with an input file
- run < <(printf '[ToInject]')
  - allows to run with injected input into stdin
- command
  - allows to execute a command when the breakpoint is hit
  - ends with end
  - ex:
  ```
    command 1
        set $rdi = 0xdeadbeef
        echo "hello world"
        x/10x $rdi
    end
  ```

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

## Baremetal
### Reset Vector
- The reset vector are the very first instructions that are executed when the system boots

### Entry Point
- The entry point can be found from the Reset vector
  - Either the start call is [ResetVector] -> [C Runtime] -> [main] or directly [C Runtime] -> [main]
    - Basically use the C Runtime as the Reset Vector
  - At the start of the program, the stack pointer is initialized
  - If we find a function that sets the stack pointer to a high address, that is likely the entry point

### Flattened Device Tree (FDT)
- Used in embedded systems to describe the hardware/peripherals
- Usually passed to the kernel at boot time
- We can use QEMU to dump the FDT and the device-tree-compiler package to decompile it
  - sudo apt install device-tree-compiler
  - qemu-system-[ARCH] -machine [MACHINE],dumpdtb [FILE.dtb] -nographic
  - dtc -I dtb -O dts FDT.dtb > out.dts

### QEMU
- -kernel option:
  - Load a ELF in memory and jump to the entry point
- -device option:
  - Allows to load an executable or raw binary
  - Allows to set the instruction pointer to a specific address
  - if we want to run raw binary, add force-raw=on
- -bios option:
  - opensbi can cause problems with some firmwares
  - use -bios none to disable it
### GDB
- we can use -s to expose GDB on port 1234 and -S to wait for GDB connection before starting the CPU
- gdb-multiarch for cross architecture debugging 
- set architecture [ARCH] in GDB to set the architecture
- target extended-remote 127.0.0.1:1234 to connect to QEMU
