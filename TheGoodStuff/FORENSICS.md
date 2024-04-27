[BACK](../README.md)
# Forensics

## Rust_file_crawler
`rust_file_crawler.exe [folder] -c`
## Sleuth

Useful to do forensics on .img/.iso files

### If we get "Cannot determine file system type"
We need to pass in an offset -> add `-o [offset]` to the command

To get offsets on the image:
`mmls [img]`
Example result: ![Alt text](image-1.png)

To get info on an image:
`fsstat [img]` 

To find a file in the image:
`fls -r [img] | grep [filename]` <-- will give the inode of the file

To read the content of the file:
`icat [img] [inode]`
