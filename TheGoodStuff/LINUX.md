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
## Get info about ELF files:
`readelf [file]`

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

