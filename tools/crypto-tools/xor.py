from itertools import product
from math import prod

from utils import (
    NONE_DISPLAY,
    default_display,
    get_default_arg_parser,
    hamming_distance,
    parse_display,
    parse_enc,
    parse_byte_arg,
)





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
            block = b""
            for j in range(i, len(enc), key_size):
                block += bytes([enc[j]])
            res = try_single_char_xor(block, NONE_DISPLAY)
            b = []
            for idx, j in enumerate(res):
                if histogram_value(j) > 0.35:
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
    encs = parse_enc(arguments.enc, arguments.file, arguments.split, arguments.type)
    display = parse_display(arguments.display)

    if not arguments.brute_force:
        key = parse_byte_arg(arguments.key, arguments.key_type, "Key is required")
        for enc in encs:
            xor(key, enc, display)
        return

    if arguments.unknown_key_size:
        for enc in encs:
            break_repeating_key_xor(enc, display)
        return

    for enc in encs:
        try_single_char_xor(enc, display)


if __name__ == "__main__":
    arg_parser = get_default_arg_parser("XOR utility")
    arg_parser.add_argument(
        "--brute-force",
        "-b",
        help="Brute force the key",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "--unknown-key-size",
        "-u",
        help="Unknown key size for brute force",
        action="store_true",
    )

    arguments = arg_parser.parse_args()
    run(arguments)
