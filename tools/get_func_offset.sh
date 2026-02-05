#! /bin/bash
if [ -z "$1" ]
then
    echo "Pass an elf file path"
    exit
fi
if [ -z "$2" ]
then
    echo "Pass a function name"
    exit
fi

# Function Virtual Address (VA):
fva="0x$(readelf -s $1 | grep $2 | grep -o -P '[0-9a-fA-F]{16}')"

# .text section Offset:
tso="0x$(readelf -S $1 | grep .text | grep -o -P '[0-9a-fA-F]{8}$')"

# .text section VA:
tsva="0x$(objdump -h $1 | grep .text | grep -o -P '[0-9a-fA-F]{8}[ ]+[0-9a-f]{16}' | grep -o -P '[0-9a-fA-F]{16}')" 

printf "0x%X\n" $(($fva - $tsva + $tso))