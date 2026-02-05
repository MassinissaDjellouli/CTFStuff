#!/usr/bin/python3

from contextlib import contextmanager

from pwn import *

context(log_level="debug")
context.terminal = ["tmux", "split-window", "-h"]

FILE = "/challenge/ello-ackers"
HOST, PORT = "chals.ctf.csaw.io", 21006
PAYLOAD_SIZE = 0xF0




def br(func, off=0):
    return f"b *"+func + " + " + off

def gdb_script(*args):
    return "\n".join(args) + "\n"

gdbscript = gdb_script(
    br(""),
)



@contextmanager
def launch(local=True, debug=False, aslr=False, argv=None, envp=None):
    target = None

    try:
        if local:
            global exe

            context.binary = exe
            
            target = process([exe.path], env=envp,aslr=aslr)
            log.info(f"PID: "+ str(target.pid))
            if debug:
                gdb.attach(target, gdbscript=gdbscript)
        else:
            target = remote(HOST, PORT)
        yield target
    finally:
        if target:
            target.close()


def main():
    try:
        with launch(debug=True) as target:
            if attack(target):
                log.success("Attack completed successfully.")
            else:
                log.failure("Attack did not yield a flag.")
    except Exception as e:
        log.exception(f"An error occurred in main: " + str(e))

def attack(io):
    io.interactive()
    return True

if __name__ == "__main__":
    main()
