## General tips
- When checking for vulnerabilities:
  - try finding the program's version
  - Try checking if CVEs exist for that version
  - Try checking if a github public repo exists for the program
    - Check the commits for the version you found
    - Check the commits for the versions after the one you found
    - Check changelogs
- Try to find the end goal first, and work backwards
- Apparently twitter is a goldmine for mini exploits
- When you have a docker container, go in the shell and check the versions of the programs installed

## Snowflake 

Discord & Twitter
```
111111111111111111111111111111111111111111 11111 11111 111111111111
64                                         22    17    12          0
```
63-22 (42 bits) - timestamp
21-17 (5 bits) - datacenter id
16-12 (5 bits) - worker id
11-0  (12 bits) - sequence number
### Discord snowflake decoder
https://snowsta.mp/

## Base64

b64decode does not take spaces into account
    ZmxhZy10aGlzaXNiNjQ= is the same as ZmxhZy10a GlzaXNiNjQ=
If we are comparing a string with base64, we can add spaces to control the result of the comparaison

## ImageMagick 
- Versions before 6.9.3-9 are vulnerable to RCE
  - Multiple examples exist for ImageTragick
  - https://imagetragick.com/
- Convert arguments:
  - TEXT:[FILE] -> writes the content of FILE as text on the image
  - -write [FILE] -> writes the content of the image to FILE