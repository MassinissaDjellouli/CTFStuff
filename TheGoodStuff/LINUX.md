[BACK](../README.md)
# Linux

Move from ssh to main computer:
```bash
scp -P [PORT] user@host:path /mnt/c/Users/...
```

```bash
sudo -l #list actions that you can do
sudo -u [user] #impersonate user
```

If you are allowed to do a command on a path ending with /*, you can execute it anywhere
## ELF files:
- Get info about an elf file: `readelf [file]`
- [Diagram of an elf file structure](img/ELF_Executable_and_Linkable_Format_diagram_by_Ange_Albertini.png) 
## Unix bins that can bypass security stuff
https://gtfobins.github.io/

checksec:
Shows the security information on a file.
useful for pwn challenges 

## Useful to search:
- .php files
- .html/.js/.css
- .db files
- ./ssh
    - id_rsa <- private key
- ./etc ./www
- .config files
- .log files
- grep -r "tofind" 2>/dev/null 
  - search in all the files in a folder
- find / -readable -and -user [user] 2>/dev/null | grep -v 'proc' | grep -v 'sys'
### ex:
    
    User x may run the following commands on host_machine:
    /bin/cat /x/public/* 
                       
    this means you can do something like: cat /x/public/../../user2/flag.txt

## SUID exploits

If file permission has: -##s##### (s instead of x for root permission) -> <strong>SUID</strong>

### 1. Change PATH variable
#### Example:
```bash
ls flag.txt
```
#### Exploit by:
```bash
cp /bin/cat /tmp/ls #if there are arguments after the ls, try using nano instead
export PATH=/tmp 
```
### 2. Pass a symlink to a file
### File descriptors:
    STDIN = 0
    STDOUT = 1
    STDERR = 2

### Cat file without putting spaces:
`cat</path/to/file`

### Pass commands as input
If eval is used:
- Pass command in between ``
  
### Bypass &>/dev/null
- eval $(command) 2>&0
  - execute the command
  - tries to execute the result
  - fails unless the result is a command
  - prints to stderr the result of the command
  - redirects stderr to stdin

### Bypass characters
- use ? for one or 2 unknown chars in paths
- {startchar..endchar}\ can be used to loop through the characters in the interval
  - ex: b and s are not allowed in the input, trying to launch bash:
    - eval {a..c}a{r..t}h\;
  
## Conditionals:

- -eq -> compare numbers
- [  ] -> equivalent to test
- -z -> empty string
- -n -> not empty string
- -e -> file exists
- -f -> file exists and is a regular file
- -d -> file exists and is a directory
- -r -> file is readable
- -w -> file is writable
- -x -> file is executable
- -o -> or
- -a -> and
- -gt -> greater than
- -lt -> less than
- -ge -> greater or equal
- -le -> less or equal
- -ne -> not equal

### Unquoted expression injection
if we use test or [   ] with an argument that is not quoted, we can inject conditinals
```bash
[ $VAR -eq $1 ] #we can pass something like 1 -o 1 -eq 1 to return true
```

### Useful commands:
- `echo -n` -> no newline
- `cut -d [delimiter] -f [index]` -> cut by delimiter and get input at index (Starts at 1)
- `cut -c [start]-[end]` -> cut by character
- `tr -d [char]` -> delete all instance of [char]
- `tr -s [char_array] [char]` -> replace all char in [char_array] with [char]
- `xxd -r -p` -> convert hex to ascii