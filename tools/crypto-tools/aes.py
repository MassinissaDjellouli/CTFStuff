from Crypto.Cipher import AES
from utils import (
    NONE_DISPLAY,
    get_default_arg_parser,
    parse_display,
    parse_enc,
    parse_key,
)

def pad_pkcs7(data: bytes, block_size: int) -> bytes:
    padding = block_size - len(data) % block_size
    return data + bytes([padding] * padding)

def count_aes_ecb_repetitions(ciphertext):
    chunks = [
        ciphertext[i : i + AES.block_size] for i in range(0, len(ciphertext), AES.block_size)
    ]
    number_of_duplicates = len(chunks) - len(set(chunks))
    return number_of_duplicates


def detect_ecb_encrypted_ciphertext(ciphertexts):
    best = (-1, 0)
    for i in range(len(ciphertexts)):
        repetitions = count_aes_ecb_repetitions(ciphertexts[i])
        best = max(best, (i, repetitions), key=lambda t: t[1])
    return best


def ecb_decrypt(key: bytes, data: bytes, display=NONE_DISPLAY) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    if display is NONE_DISPLAY:
        return cipher.decrypt(data)
    return display(cipher.decrypt(data), key)

def ecb_encrypt(key: bytes, data: bytes, display=NONE_DISPLAY) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    if display is NONE_DISPLAY:
        return cipher.encrypt(data)
    return display(cipher.encrypt(data), key)

def decode_mode(enc: bytes):
    if count_aes_ecb_repetitions(enc) > 0:
        return ecb_decrypt
    return lambda _, __, display: display(b"Not implemented", b"\x00")

def encrypt(arguments):
    aes_type = arguments.aes_type
    encs = parse_enc(arguments.enc, arguments.file, arguments.split, arguments.type)
    key = parse_key(arguments.key, arguments.key_type)
    display = parse_display(arguments.display)
    for enc in encs:
        match aes_type:
            case "ecb":
                print("ECB mode")
                print(ecb_encrypt(key, enc, display))
            case "auto":
                print("Auto mode not supported for encryption")
                exit(1)
            case _:
                print("Unknown mode")
                exit(1)

def decrypt(arguments):
    aes_type = arguments.aes_type
    encs = parse_enc(arguments.enc, arguments.file, arguments.split, arguments.type)
    key = parse_key(arguments.key, arguments.key_type)
    display = parse_display(arguments.display)
    for enc in encs:
        match aes_type:
            case "ecb":
                print(ecb_decrypt(key, enc, display))
            case "auto":
                decode = decode_mode(enc)
                decode(key, enc, display)
            case _:
                print("Unknown mode")
                exit(1)
                
def run(arguments):
    if arguments.encrypt:
        encrypt(arguments)
        return
    decrypt(arguments)
    


if __name__ == "__main__":
    arg_parser = get_default_arg_parser("AES utility")
    arg_parser.add_argument(
        "--aes-type", "-a", help="AES type", default="ecb", choices=["ecb", "auto"]
    )
    arg_parser.add_argument(
        "--encrypt",
        "-e",
        help="Encrypt data",
        action="store_true",
        default=False,
    )
    arguments = arg_parser.parse_args()
    run(arguments)
