import random
from Crypto.Cipher import AES
from utils import (
    NONE_DISPLAY,
    get_default_arg_parser,
    parse_display,
    parse_enc,
    parse_byte_arg,
)

from xor import xor

def pad_pkcs7(data: bytes, block_size: int) -> bytes:
    padding = block_size - len(data) % block_size
    return data + bytes([padding] * padding)

def unpad_pkcs7(data: bytes) -> bytes:
    padding = data[-1]
    if padding == 0 or padding > len(data):
        return data
    if not all(x == padding for x in data[-padding:]):
        return data
    return data[:-padding]

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


def ecb_decrypt(key: bytes, data: bytes, display=NONE_DISPLAY,unpadder=unpad_pkcs7) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    if display is NONE_DISPLAY:
        return cipher.decrypt(data)
    return display(unpadder(cipher.decrypt(data)), key)

def ecb_encrypt(key: bytes, data: bytes, display=NONE_DISPLAY,padder=pad_pkcs7) -> bytes:
    data = padder(data, AES.block_size)
    cipher = AES.new(key, AES.MODE_ECB)
    if display is NONE_DISPLAY:
        return cipher.encrypt(data)
    return display(cipher.encrypt(data), key)

def cbc_encrypt(key: bytes, data: bytes, iv: bytes, display=NONE_DISPLAY,padder=pad_pkcs7) -> bytes:
    data = padder(data, AES.block_size)
    blocks = [data[i : i + AES.block_size] for i in range(0, len(data), AES.block_size)]
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b""
    previous_block = iv
    for block in blocks:
        xored = xor(previous_block, block, NONE_DISPLAY)
        previous_block = cipher.encrypt(xored)
        ciphertext += previous_block
    if display is NONE_DISPLAY:
        return ciphertext
    display(ciphertext, key)
    
def cbc_decrypt(key: bytes, data: bytes, iv: bytes, display=NONE_DISPLAY,unpadder=unpad_pkcs7) -> bytes:
    blocks = [data[i : i + AES.block_size] for i in range(0, len(data), AES.block_size)]
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = b""
    previous_block = iv
    for block in blocks:
        decrypted = cipher.decrypt(block)
        xored = xor(previous_block, decrypted,NONE_DISPLAY)
        plaintext += xored
        previous_block = block
    plaintext = unpadder(plaintext)
    if display is NONE_DISPLAY:
        return plaintext
    display(plaintext, key)
def decode_mode(enc: bytes):
    if count_aes_ecb_repetitions(enc) > 0:
        return ecb_decrypt
    return lambda _, __, display: display(b"Not implemented", b"\x00")

def encrypt(arguments):
    aes_type = arguments.aes_type
    encs = parse_enc(arguments.enc, arguments.file, arguments.split, arguments.type)
    key = parse_byte_arg(arguments.key, arguments.key_type,"Key is required")
    display = parse_display(arguments.display)
    for enc in encs:
        match aes_type:
            case "ecb":
                print("ECB mode")
                print(ecb_encrypt(key, enc, display))
            case "cbc":
                print("CBC mode")
                iv = parse_byte_arg(arguments.iv, arguments.iv_type,"IV is required")
                cbc_encrypt(key, enc, iv, display)
            case "auto":
                print("Auto mode not supported for encryption")
                exit(1)
            case _:
                print("Unknown mode")
                exit(1)

def decrypt(arguments):
    aes_type = arguments.aes_type
    encs = parse_enc(arguments.enc, arguments.file, arguments.split, arguments.type)
    key = parse_byte_arg(arguments.key, arguments.key_type, "Key is required")
    display = parse_display(arguments.display)
    for enc in encs:
        match aes_type:
            case "ecb":
                print(ecb_decrypt(key, enc, display))
            case "cbc":
                iv = parse_byte_arg(arguments.iv, arguments.iv_type, "IV is required")
                cbc_decrypt(key, enc, iv, display)
            case "auto":
                decode = decode_mode(enc)
                decode(key, enc, display)
            case _:
                print("Unknown mode")
                exit(1)
            
def encryption_oracle(data: bytes) -> bytes:
    key = random.randbytes(AES.block_size)    
    append_count = random.randint(5, 10)
    mode = random.choice(["ecb", "cbc"])
    data = random.randbytes(append_count) + data + random.randbytes(append_count)
    match mode:
        case "ecb":
            print("ECB mode")
            return ecb_encrypt(key, data)
        case "cbc":
            print("CBC mode")
            iv = random.randbytes(AES.block_size)
            return cbc_encrypt(key, data, iv)
        case _:
            print("Unknown mode")
            exit(1)
            
def ecb_or_cbc(enc: bytes) -> str:
    return "ecb" if count_aes_ecb_repetitions(enc) > 0 else "cbc"

def run(arguments):
    if arguments.encrypt:
        encrypt(arguments)
        return
    decrypt(arguments)
    
def run_encryption_oracle(arguments):
    parsed_enc = parse_enc(arguments.enc)
    enc = encryption_oracle(parsed_enc[0])
    print(f"Guessed mode: {ecb_or_cbc(enc)}")

if __name__ == "__main__":
    arg_parser = get_default_arg_parser("AES utility")
    arg_parser.add_argument(
        "--aes-type", "-a", help="AES type", default="ecb", choices=["ecb","cbc", "auto"]
    )
    arg_parser.add_argument(
        "--encrypt",
        "-e",
        help="Encrypt data",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "--iv",
        "-i",
        help="Initialization vector",
        default="",
    )
    arg_parser.add_argument(
        "--iv-type",
        "-I",
        help="Initialization vector type",
        default="h",
        choices=["h", "b", "s"],
    )
    arg_parser.add_argument(
        "--oracle",
        "-o",
        help="Run encryption oracle",
        action="store_true",
    )
    arguments = arg_parser.parse_args()
    if arguments.oracle:
        run_encryption_oracle(arguments)
    else:
        run(arguments)
