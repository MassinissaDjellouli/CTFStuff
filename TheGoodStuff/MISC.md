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