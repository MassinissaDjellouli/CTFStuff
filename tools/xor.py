from argparse import ArgumentParser
from nostril import nonsense

def from_str(string: str) -> bytes:
    return bytes(string, "utf-8")


def from_hex(string: str) -> bytes:
    return bytes.fromhex(string)


def from_numeric(string: str) -> bytes:
    return bytes([int(x) for x in string.replace("[", "").replace("]", "").split(",")])

def nonsense_check(enc: bytes):
    try :
        return nonsense(enc.decode("latin-1"))
    except:
        return True
def default_display(enc: bytes, key:str):
    print(f"Key: {key.hex()}")
    print(enc.decode("latin-1"))

def word_display(enc: bytes, key:str):
    if not nonsense_check(enc):
        print(f"Key: {key.hex()}")
        print(enc.decode("latin-1"))

def hex_display(enc: bytes, key:str):
    print(f"Key: {key.hex()}")
    print(enc.hex())


def numeric_display(enc: bytes, key:str):
    print(f"Key: {key.hex()}")
    print([int(x) for x in enc])


def xor(key: bytes, enc: bytes, display=default_display):
    display(bytes([x ^ key[i % len(key)] for i, x in enumerate(enc)]), key)


def try_single_char_xor(enc: bytes, display=default_display):
    for i in range(1,256):
        xor(from_numeric(str(i)), enc,display)


p = ArgumentParser(description="XOR utility", add_help=True)

p.add_argument("enc", help="Encrypted data")
p.add_argument("--file", "-f", help="File with encrypted data", action="store_true", default=False)
p.add_argument("--key", "-k", help="Key to use for XOR")
p.add_argument(
    "--brute-force","-b", help="Brute force the key", action="store_true", default=False
)
p.add_argument(
    "-d",
    "--display",
    help="Display format: d (default), h (hex), n (numeric), w (word)",
    default="d",
    choices=["d", "h", "n", "w"],
)
p.add_argument(
    "-t",
    "--type",
    help="Type of encrypted data: s (string), h (hex), n (numeric)",
    default="s",
    choices=["s", "h", "n"],
)
p.add_argument(
    "-kt",
    "--key-type",
    help="Type of key: s (string), h (hex), n (numeric)",
    default="s",
    choices=["s", "h", "n"],
)

arguments = p.parse_args()
encs = []
if arguments.file:
    with open(arguments.enc, "r") as f:
        enc_file = f.read()
        enc_strs = enc_file.strip().split("\n")
        for enc in enc_strs:
            match arguments.type:
                case "s":
                    encs.append(from_str(enc))
                case "h":
                    encs.append(from_hex(enc))
                case "n":
                    encs.append(from_numeric(enc))
                case _:
                    encs.append(from_str(enc))
else:
    match arguments.type:
        case "s":
            encs.append(from_str(arguments.enc))
        case "h":
            encs.append(from_hex(arguments.enc))
        case "n":
            encs.append(from_numeric(arguments.enc))
        case _:
            encs.append(from_str(arguments.enc))

display = default_display
match arguments.display:
    case "h":
        display = hex_display
    case "n":
        display = numeric_display
    case "w":
        display = word_display
    case _:
        display = default_display

if arguments.brute_force:
    for enc in encs:
        try_single_char_xor(enc, display)
    exit(0)

key = bytes()
match arguments.key:
    case None:
        print("Key is required")
        exit(1)
    case _:
        key = bytes()
        match arguments.key_type:
            case "s":
                key = from_str(arguments.key)
            case "h":
                key = from_hex(arguments.key)
            case "n":
                key = from_numeric(arguments.key)
            case _:
                key = from_str(arguments.key)

for enc in encs:
    xor(key, enc, display)
 