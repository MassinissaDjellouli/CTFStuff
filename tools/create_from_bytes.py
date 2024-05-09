import datetime
from os import popen
byt = b''
extension = ""
path = popen("getPath").readline().replace("\n","")

file = open(path + "/tmp/" + str(datetime.datetime.now().timestamp()) + extension,'wb')
file.write(byt)