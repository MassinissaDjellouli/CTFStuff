import subprocess
from os import listdir
from os.path import isfile, join

cmd = "md5sum"
filePath = "/mnt/d/Pictures"
onlyfiles = [f for f in listdir(filePath) if isfile(join(filePath, f))]
for i in onlyfiles:
    outa = subprocess.Popen([cmd,i], stdout=subprocess.PIPE,text=True)
    print(outa.stdout.read())