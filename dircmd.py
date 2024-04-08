import subprocess
import sys
from os import listdir
from os.path import isfile, join
if sys.argv[1] == '-h':
    print('''
    Usage: dircmd.py [command [args]] [Path]
''')
    exit(0)
if len(sys.argv) < 3:
    print("Need to pass in the command and path as arguments")
    exit(1)
cmd = sys.argv[1]
args = sys.argv[2:-1] if len(sys.argv) > 3 else []
filePath = sys.argv[-1]
onlyfiles = [f for f in listdir(filePath) if isfile(join(filePath, f))]
for i in onlyfiles:
    arguments = [cmd] + [x for x in args] + [i]
    outa = subprocess.Popen(arguments, stdout=subprocess.PIPE,text=True)
    try:
        print(outa.stdout.read())
    except:
        print("Could not print {''.join(arguments,' ')}")