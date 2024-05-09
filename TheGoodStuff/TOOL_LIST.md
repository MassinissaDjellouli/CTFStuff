# DISCLAIMER
## All of this was made for my setup, might not work for yours.

## BEFORE USING:
1. Set the right paths in getPath, getWindowsPath and getJavaPath.
   - Set the jre1.8/bin path in getJavaPath
   - Set the path to CTFStuff (This repo) in getPath (Linux path) and getWindowsPath (Windows path)
2. run init.sh

## Windows/WSL only:
- apngdis_gui.exe
  - Can be used to dissasemble and manipulate .apng files
- gdre_tools.exe
  - Godot reverse tools
- imganalyzer.exe
  - Allows to manipule jpg pictures
- openstego.sh
  - Launches openstego from WSL
- rust_file_crawler.exe
  - Can search files in a directory
  - Can read file content by adding -c at the end
  - Works once every 5 times
  - Just use the find command
- d2jar.sh
  - dex to jar 
  - Pass a path to a apk file

## Linux/WSL only:
- crackJWT.sh
  - requires: 
    - https://github.com/lmammino/jwt-cracker
  - Pass a token and it cracks it using rockyou
- find_in.sh
  - Find a string in a directory
  - Pass a directory and a string
- get_func_offset.sh
  - Find the hex offset of a function in an ELF file.
- peepdf
  - requires python2
  - runs peepdf
  - allows you to explore pdf streams and objects
- plainsight_decode.sh
  - requires python2
  - run setup_plainsight.sh before running plainsight_decode.sh for the first time
  - allows you to convert a plainsight ciphered text to clear text
## Linux + Windows/WSL
- edit_flask_token.sh
  - pip install flask-unsign
  - Allows you to edit a flask token by passing the secret
- crack_flask_token.sh
  - pip install flask-unsign
  - Find the secret for a flask token
- dircmd.py
  - Runs a command on every file in a directory
- create_from_bytes
  - Creates a file in CTFStuff/tmp
  - Change the byt variable with the bytes to write in hex
  - Change the extension variable with the desired extension
- xor.py
  - Does xor
- bmpextender.py
  - Extends a bmp image to reveal hidden content
- mqtt.py
  - Communicate with a mqtt server
  - Modify the file as needed
- nc.py
  - Communicate with netcat line by line
  - Modify the file as needed