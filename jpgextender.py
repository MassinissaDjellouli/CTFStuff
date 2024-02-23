import argparse

path="tunn3l_v1s10n.bmp"
with open(path, "rb") as f:
    lines = f.readlines()

argparser = argparse.ArgumentParser()
argparser.add_argument('filename', help="File", type=str)
argparser.add_argument("-H", "--height", help="height to add to the image. DEFAULT=512",default=512, type=int, required=False)
argparser.add_argument("-w", "--width", help="width to add to the image. DEFAULT=0",default=0, type=int, required=False)
argparser.add_argument("-s", "--silent", help="No logs or confirmation", action="store_true", required=False)
argparser.add_argument("-f", "--force", help="No confirmation", action="store_true", required=False)
args = argparser.parse_args()

toAddWidth = args.width
toAddHeight = args.height
headerLength = 16
hdrWidthOffset = 0
hdrHeightOffset = 4
widthSize = 4
heightSize = 4
i = 0
a = []
for x in [*lines[0]]:
    if i > headerLength + hdrWidthOffset + widthSize:
        break
    if i > headerLength + hdrWidthOffset :
        a.append(x)
    i+=1
width = int.from_bytes(a, byteorder='little')
i = 0
a = []
for x in [*lines[0]]:
    if i > headerLength + hdrHeightOffset + heightSize:
        break
    if i > headerLength + hdrHeightOffset:
        a.append(x)
    i+=1
height = int.from_bytes(a, byteorder='little')
newWidth = width + toAddWidth
newHeight = height + toAddHeight
newWidthBytes = newWidth.to_bytes(4, byteorder='little')
newHeightBytes = newHeight.to_bytes(4, byteorder='little')
if not args.silent:
    print("New width: " + str(newWidth))
    print("New height: " + str(newHeight))
    if not args.force:
        print("Continue? (y/n)")
        if input() != "y" and input() != "Y" and input() != "":
            exit()
with open(path, "r+b") as f:
    f.seek(headerLength + hdrWidthOffset + 1)
    f.write(newWidthBytes)
    f.seek(headerLength + hdrHeightOffset + 1)
    f.write(newHeightBytes)
    f.close()
if not args.silent:
    print("Done!")
