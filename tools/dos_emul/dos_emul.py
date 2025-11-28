import os
import shutil
from argparse import ArgumentParser
from time import sleep
import pexpect 
tools_dir = os.getenv("CTF_STUFF", "") + "/tools"
if not os.path.isdir(tools_dir):
    raise EnvironmentError("CTF_STUFF environment variable is not set correctly.")


def main():
    parser = ArgumentParser(description="Emulate a DOS program.")
    parser.add_argument(
        "root_path", type=str, help="The root path for the DOS environment"
    )
    parser.add_argument("program_path", type=str, help="The DOS program to run")
    args = parser.parse_args()
    root_path = args.root_path
    program = args.program_path
    qemu = [
        "qemu-system-i386",
        "-hda",
        f"{tools_dir}/dos_emul/dos.qcow2",
        "-m",
        "16M",
        "-drive",
        f"file=fat:rw:{root_path},format=raw,media=disk",
        "-serial",
        "mon:stdio",
    ]
    if not os.path.isdir(root_path):
        print(f"Error: The specified root path '{root_path}' is not a valid directory.")
        return
    if not os.path.isfile(os.path.join(root_path, program)):
        print(
            f"Error: The specified program '{program}' does not exist in the root path."
        )
        return

    if not os.path.isfile(root_path + "/dos_emul/DEBUGX.COM"):
        shutil.copyfile(
            os.path.join(tools_dir + "/dos_emul/DEBUGX.COM"), root_path + "/DEBUGX.COM"
        )

    p = pexpect.spawn(" ".join(qemu))
    p.sendline("1")
    p.expect("C:\\>", timeout=60)
    print("DOS Prompt Ready.")
    p.sendline("DIR")
    p.expect("C:\\>", timeout=10)
    print("Output of DIR:")
    print(p.before.decode(errors="ignore"))

if __name__ == "__main__":
    main()
