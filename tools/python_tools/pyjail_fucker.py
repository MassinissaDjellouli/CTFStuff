import argparse
import re

FULL_W = "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"
REG = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAPPED_ALPHABET = zip(REG, FULL_W)

TRUE = "[[]]>[]"
FALSE = "[]>[]"

DOUBLE_ = "_＿"


def craft_num(n):
    """
    craft symbol-only numbers, in an inefficient way
    """
    str_0 = "[].__len__()"
    str_1 = "[x].__len__()"
    if n == 0:
        return str_0
    ret = f"{str_1.replace("x",",".join(["()"]*n))}"
    return ret

# no_chr cant craft k or x 
def craft_chr(n: str, no_chr: bool = False) -> str:
    if not no_chr:
        return f"chr({ord(n)})"
    upper = n.isupper()
    n = n.lower()
    s = [].__doc__
    letter_to_idx1 = {}
    for i in s:
        if i not in letter_to_idx1:
            letter_to_idx1[i] = s.index(i)
    s = ().__doc__
    letter_to_idx2 = {}
    for i in s:
        if i not in letter_to_idx2:
            letter_to_idx2[i] = s.index(i)

    if n in letter_to_idx1:
        return (
            "[].__doc__[" + str(letter_to_idx1[n]) + "]" + (".upper()" if upper else "")
        )
    return "().__doc__[" + str(letter_to_idx2[n]) + "]" + (".upper()" if upper else "")


def craft_str(s: str, no_plus: bool = False, no_chr: bool = False) -> str:
    if not no_plus:
        return "+".join([craft_chr(x, no_chr) for x in s])

    mod = [craft_chr(x, no_chr) for x in s]
    s1 = mod.pop(0)
    mod = [f".__add__({x})" for x in mod]
    return s1 + "".join(mod)


def replace_strings(content: str, restrictions:tuple) -> str:
    content = re.sub(r"\"(.*?)\"", lambda x: craft_str(x.group(1), restrictions[0],restrictions[1]), content)
    content = re.sub(r"'(.*?)'", lambda x: craft_str(x.group(1), restrictions[0],restrictions[1]), content)
    return content


def replace_bools(content: str) -> str:
    content = content.replace("True", TRUE)
    content = content.replace("False", FALSE)
    return content


def replace_text(content: str) -> str:
    for r, f in MAPPED_ALPHABET:
        content = content.replace(r, f)
    content = content.replace("__", DOUBLE_)
    return content


def replace_numbers(content: str) -> str:
    return re.sub(r"\d+", lambda x: craft_num(int(x.group(0))), content)


def replace_content(content: str, args: tuple, restrictions:tuple) -> str:
    bools, text, numbers, strings = args
    if bools:
        content = replace_bools(content)
    if strings:
        content = replace_strings(content, restrictions)
    if numbers:
        content = replace_numbers(content)
    if text:
        content = replace_text(content)
    return content


parser = argparse.ArgumentParser()
parser.add_argument("input_filepath", type=str, help="path to the file to be modified")
parser.add_argument(
    "-b", "--booleans", action="store_true", help="replace booleans", default=False
)
parser.add_argument(
    "-t", "--text", action="store_true", help="replace text", default=False
)
parser.add_argument(
    "-n", "--numbers", action="store_true", help="replace numbers", default=False
)
parser.add_argument(
    "-s", "--string", action="store_true", help="replace strings", default=False
)
parser.add_argument(
    "-i", "--inline", action="store_true", help="inline mode", default=False
)
parser.add_argument(
    "-np",
    "--no-plus",
    action="store_true",
    help="no plus in string replacement",
    default=False,
)
parser.add_argument(
    "-nc",
    "--no-chr",
    action="store_true",
    help="no chr in string replacement",
    default=False,
)
parser.add_argument("-o", "--output_filepath", type=str, help="path to the output file")

args = parser.parse_args()

arg_tuple = (args.booleans, args.text, args.numbers, args.string)
restriction_tuple = (args.no_plus, args.no_chr)
if all(x is False for x in arg_tuple):
    arg_tuple = tuple([True] * len(arg_tuple))
if all(x is False for x in restriction_tuple):
    restriction_tuple = tuple([False] * len(restriction_tuple))
content = ""
output_filepath = args.output_filepath
if not args.inline:
    if args.input_filepath.endswith(".py") is False:
        raise ValueError("The input file must be a .py file")
    output_filepath = (
        args.input_filepath.replace(".py", "_pyjailfk.py")
        if output_filepath is None
        else output_filepath
    )
    if output_filepath.endswith(".py") is False:
        output_filepath += ".py"

    with open(args.input_filepath, "r") as f:
        content = f.read()
else:
    content = args.input_filepath

content = replace_content(content, arg_tuple, restriction_tuple)
if output_filepath is None:
    print(content)
    exit(0)

with open(output_filepath, "w") as f:
    f.write(content)
print(f"{args.input_filepath} has been modified and saved to {output_filepath}")
