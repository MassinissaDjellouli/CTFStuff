#!/usr/bin/python3

from contextlib import contextmanager

from pwn import *

context(log_level="debug")
context.terminal = ["tmux", "split-window", "-h"]

HOST, PORT = "localhost", 1337

{bindings}

def b(addr):
    addr += 0x400000
    main = 0x40xxxx
    off = addr - main
    return "b * $main + " + str(off)

def br(func, off=0):
    return f"b *"+ func + " + " + str(off)

def gdb_script(*args):
    return "\n".join(args) + "\n"

gdbscript = gdb_script(
    "ni 35",
    br("__libc_start_main", 0x84),
    "c",
    "si",
    "ni 23",
    "si",
    "set $main=(long)$rip",
    "c"
)

# gdbscript = gdb_script(
#    br("main"),
#)



@contextmanager
def launch(is_remote=False, debug=False, aslr=False, argv=None, envp=None):
    global target    
    target = None

    try:
        if not is_remote:
            global {bin_name}

            context.binary = {bin_name}
            
            if debug:
                target = gdb.debug({proc_args} + (argv or []), gdbscript=gdbscript)
                log.info(f"PID: "+ str(target.pid))
            else:
                target = process({proc_args} + (argv or []), env=envp,aslr=aslr)
        else:
            target = remote(HOST, PORT)
        yield target
    finally:
        if target:
            target.close()


def main():
    try:
        with launch(debug=True):
            if attack():
                log.success("Attack completed successfully.")
            else:
                log.failure("Attack did not yield a flag.")
    except Exception as e:
        log.exception(f"An error occurred in main: " + str(e))

def attack():
    target.interactive()
    return True

if __name__ == "__main__":
    main()
