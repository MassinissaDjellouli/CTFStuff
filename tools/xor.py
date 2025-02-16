from argparse import ArgumentParser
from base64 import b64decode
from itertools import combinations, product, zip_longest
from math import prod

from nostril import nonsense


def from_str(string: str) -> bytes:
    return bytes(string, "utf-8")


def from_hex(string: str) -> bytes:
    return bytes.fromhex(string)


def from_b64(string: str) -> bytes:
    return b64decode(string)


def hamming_distance(binary_seq_1, binary_seq_2):
    assert len(binary_seq_1) == len(binary_seq_2)
    dist = 0

    for bit1, bit2 in zip(binary_seq_1, binary_seq_2):
        diff = bit1 ^ bit2
        dist += sum([1 for bit in bin(diff) if bit == "1"])

    return dist


def from_numeric(string: str) -> bytes:
    return bytes([int(x) for x in string.replace("[", "").replace("]", "").split(",")])


def nonsense_check(enc: bytes):
    try:
        return nonsense(enc.decode("latin-1"))
    except:
        return True


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


def xor(key: bytes, enc: bytes, display=default_display) -> bytes | None:
    if display is NONE_DISPLAY:
        return bytes([x ^ key[i % len(key)] for i, x in enumerate(enc)])
    display(bytes([x ^ key[i % len(key)] for i, x in enumerate(enc)]), key)

def try_single_char_xor(enc: bytes, display=default_display):
    encs = []
    for i in range(1, 256):
        encs.append(xor(i.to_bytes(), enc, display))
    if display is NONE_DISPLAY:
        return encs
    for i in encs:
        display(i, i.to_bytes())

def histogram_value(enc: bytes) -> float:
    hist = {}
    penalize = 0
    common = [
        "e",
        "t",
        "a",
        "o",
        "i",
        "n",
        "s",
        "h",
        "r",
        "d",
        " ",
        "th",
        "he",
        "in",
        "er",
        "an",
        "re",
        "on",
        "at",
        "en",
        "nd",
        "the",
        "and",
        "tha",
        "ent",
        "ion",
        "tio",
        "for",
        "nde",
        "has",
        "nce",
        "edt",
    ]
    enc = enc.decode("latin-1")
    for c in common:
        hist[c] = enc.count(c)
    for i in enc:
        i = ord(i)
        if i < 32 or i > 126:
            penalize += 2
        if (i < 65 or i > 122) and i not in [
            32,
            33,
            44,
            46,
            58,
            59,
            63,
            39,
            34,
            45,
            40,
            41,
            123,
            125,
        ]:
            penalize += 0.5
    return (sum(hist.values()) - penalize) / len(enc)


def merge_strings(*strings):
    merged = "".join(
        filter(
            None, ("".join([chr(char) for char in chars]) for chars in zip(*strings))
        )
    )
    return merged.encode("latin-1")


def generate_combinations(lists):
    return list(product(*lists))


def get_combination_size(lists):
    return prod(len(sublist) for sublist in lists)


def break_repeating_key_xor(enc: bytes, display=default_display):
    hamming_res = {}
    for i in range(2, min(41, len(enc) // 2)):
        enc1 = enc[:i]
        enc2 = enc[i : i * 2]
        hamming = hamming_distance(enc1, enc2)
        hamming_res[i] = hamming / i
    sorted_res = sorted(hamming_res.items(), key=lambda x: x[1])
    print(f"Key sizes: {[x[0] for x in sorted_res]}")
    for key_size, _ in sorted_res:
        blocks_res = []
        for i in range(key_size):
            block = b''
            for j in range(i, len(enc), key_size):
                block += bytes([enc[j]])
            res = try_single_char_xor(block, NONE_DISPLAY)
            b = []
            for idx, j in enumerate(res):
                if histogram_value(j) > 0.4:
                    b.append((idx, j))
            blocks_res.append(b)
        if get_combination_size(blocks_res) > 10000:
            print(
                f"Too many combinations, skipping keylength {key_size} ({ get_combination_size(blocks_res)})"
            )
            continue
        zip_res = generate_combinations(blocks_res)
        for i in zip_res:
            key = bytes([x[0] + 1 for x in i])
            merged = merge_strings(*[x[1] for x in i])
            display(merged, key)


def run(arguments):
    encs = []
    if arguments.file:
        with open(arguments.enc, "r") as f:
            enc_file = f.read()
            if arguments.split:
                enc_strs = enc_file.strip().split("\n")
            else:
                enc_strs = [enc_file.strip()]
            for enc in enc_strs:
                match arguments.type:
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
        match arguments.type:
            case "s":
                encs.append(from_str(arguments.enc))
            case "h":
                encs.append(from_hex(arguments.enc))
            case "n":
                encs.append(from_numeric(arguments.enc))
            case "b":
                encs.append(from_b64(arguments.enc))
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
        if arguments.unknown_key_size:
            for i in encs:
                break_repeating_key_xor(i, display)

        else:
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


p = ArgumentParser(description="XOR utility", add_help=True)

p.add_argument("enc", help="Encrypted data")
p.add_argument(
    "--file",
    "-f",
    help="File with encrypted data",
    action="store_true",
    default=False,
)
p.add_argument("--split", "-s", help="Split data by delimiter", action="store_true")
p.add_argument("--key", "-k", help="Key to use for XOR")
p.add_argument(
    "--brute-force",
    "-b",
    help="Brute force the key",
    action="store_true",
    default=False,
)
p.add_argument(
    "--unknown-key-size",
    "-u",
    help="Unknown key size for brute force",
    action="store_true",
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
    help="Type of encrypted data: s (string), h (hex), n (numeric), b (base64)",
    default="s",
    choices=["s", "h", "n", "b"],
)
p.add_argument(
    "-kt",
    "--key-type",
    help="Type of key: s (string), h (hex), n (numeric)",
    default="s",
    choices=["s", "h", "n"],
)

arguments = p.parse_args()
if __name__ == "__main__":
    run(arguments)
