import base64
import hashlib
import os

import elftools
import elftools.elf
import elftools.elf.elffile
import requests

url = "http://challenges.ringzer0team.com:10015/"
res = requests.get(url).text.split("----- BEGIN Elf Message -----")[1]
res = res.split("----- END Elf Message -----")[0].strip()
res = res.split("<br />")[1].strip()
d = base64.b64decode(res)
try:
    while True:
        d = base64.b64decode(d.decode())
except:
    print("a")

int_values = [x for x in d]
int_values.reverse()
by = bytes(int_values)
file = open("file",'wb')
file.write(by)
file.close()

file = open("file","r+b")
elf = elftools.elf.elffile.ELFFile(file)
data = elf.get_section_by_name(".text")
start = data['sh_offset']
end = start + data['sh_size']
file.seek(start)
data = file.read(end-start)
int_values = [x for x in data]
idx = [i for i in range(len(int_values)) if int_values[i] == 2]

file.seek(start + idx[3])
file.write(b"\x00")
file.close()
res = os.popen("./file").read().strip()
print(res)
res = requests.get("http://challenges.ringzer0team.com:10015/?r=" + res).text
if "<div class=\"alert alert-danger\">" in res:
    print(res.split("<div class=\"alert alert-danger\">")[1].split("</div>")[0])
else:
    print(res.split("<div class=\"alert alert-info\">")[1].split("</div>")[0])