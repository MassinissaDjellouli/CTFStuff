from argparse import ArgumentParser
from base64 import b64decode
from nostril import nonsense
def from_str(string: str) -> bytes:
    return bytes(string, "utf-8")


def from_hex(string: str) -> bytes:
    return bytes.fromhex(string)


def from_b64(string: str) -> bytes:
    return b64decode(string)

def from_numeric(string: str) -> bytes:
    return bytes([int(x) for x in string.replace("[", "").replace("]", "").split(",")])


def default_display(enc: bytes, key: bytes):
    print(f"Key: {key.hex()}")
    print(enc.decode("latin-1"))


def word_display(enc: bytes, key: bytes):
    if not nonsense_check(enc):
        print(f"Key: {key.hex()}")
        print(enc.decode("latin-1"))


def hex_display(enc: bytes, key: bytes):
    print(f"Key: {key.hex()}")
    print(enc.hex())


def numeric_display(enc: bytes, key: bytes):
    print(f"Key: {key.hex()}")
    print([int(x) for x in enc])

def NONE_DISPLAY():
    pass

def nonsense_check(enc: bytes):
    try:
        return nonsense(enc.decode("latin-1"))
    except:
        return True

def parse_key(k,kt):
    key = bytes()
    match k:
        case None:
            print("Key is required")
            exit(1)
        case _:
            key = bytes()
            match kt:
                case "s":
                    key = from_str(k)
                case "h":
                    key = from_hex(k)
                case "n":
                    key = from_numeric(k)
                case _:
                    key = from_str(k)
    return key

def parse_enc(e, is_file = False, split = False, type = "s"):
    encs = []
    if is_file:
        with open(e, "r") as f:
            enc_file = f.read()
            if split:
                enc_strs = enc_file.strip().split("\n")
            else:
                enc_strs = [enc_file.strip()]
            for enc in enc_strs:
                match type:
                    case "s":
                        encs.append(from_str(enc))
                    case "h":
                        encs.append(from_hex(enc))
                    case "n":
                        encs.append(from_numeric(enc))
                    case "b":
                        encs.append(from_b64(enc))
                    case _:
                        encs.append(from_str(enc))
    else:
        match type:
            case "s":
                encs.append(from_str(e))
            case "h":
                encs.append(from_hex(e))
            case "n":
                encs.append(from_numeric(e))
            case "b":
                encs.append(from_b64(e))
            case _:
                encs.append(from_str(e))
    return encs

def parse_display(d):
    display = default_display
    match d:
        case "h":
            display = hex_display
        case "n":
            display = numeric_display
        case "w":
            display = word_display
        case _:
            display = default_display
    return display

def get_default_arg_parser(description):
    p = ArgumentParser(description=description, add_help=True)

    p.add_argument("enc", help="Encrypted data")
    p.add_argument(
        "--file",
        "-f",
        help="File with encrypted data",
        action="store_true",
        default=False,
    )
    p.add_argument("--split", "-s", help="Split data by line", action="store_true")
    p.add_argument("--key", "-k", help="Key to use to decrypt")

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
        help="Encoding type of encrypted data: s [DEFAULT] (string), h (hex), n (numeric), b (base64)",
        default="s",
        choices=["s", "h", "n", "b"],
    )
    p.add_argument(
        "-kt",
        "--key-type",
        help="Encoding type of key: s (string)[DEFAULT], h (hex), n (numeric)",
        default="s",
        choices=["s", "h", "n"],
    )
    return p

def hamming_distance(binary_seq_1, binary_seq_2):
    assert len(binary_seq_1) == len(binary_seq_2)
    dist = 0

    for bit1, bit2 in zip(binary_seq_1, binary_seq_2):
        diff = bit1 ^ bit2
        dist += sum([1 for bit in bin(diff) if bit == "1"])

    return dist