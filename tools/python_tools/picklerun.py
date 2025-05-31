from pickle import loads
import sys
import base64

arg = sys.argv[1]

loads(base64.b64decode(arg))