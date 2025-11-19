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
## FFMPEG
- The concat protocol can be used to join multiple input files together
  - If we want to extract data using concat:
    - concat:audio1.x|/data|/audio2.x
    - wav files can be used to store text data
    - mp3 files can be used to store binary data
  - The first file is for the header, the last file is for the extension

## JS
### Regex matching
- test():
  - if the regex uses /x/g or /x/y, the next call to test() will start searching from the last index
  - ex:
    ```javascript
    let regex = /a/g;
    console.log(regex.test("aba")); // true
    console.log(regex.test("aba")); // false
    console.log(regex.test("aba")); // true
    ```
  - This can be used to bypass filters that use regex to block certain words
    - ex: if we want to block "alert", we can use /a/g to match the first "a", then the next test() will start from the last index and will not match "lert"
