[BACK](../README.md)
# Networking

### Wireshark Captures
    
- Follow stream to read the data sent in one chunk
- `File -> Export Objects -> [Protocol]` To get all the objects sent 
- For multipart http packets:
  - MIME Multipart Media encapsulation
    - Encapsulating multipart part
      - data: (content-type) <--- right click --> Export Packet Bytes
- tshark can be used to extract data
  - tshark -r [file] -Y "[filter]" -T fields -e [fields_to_display]
    - useful fields options:
    - ip.src, ip.dst, tcp.srcport, tcp.dstport, tcp.len, tcp.seq, tcp.ack, tcp.flags, tcp.window_size, tcp.checksum, tcp.options, tcp.analysis.bytes_in_flight
    - data.data, data.len, data.data_len, data.data_offset, data.data_line, data.data_line_len, data.data_line_offset

#### Failed DNS requests:
- if we have a capture with failed DNS requests to for an interesting address:
  - Try an alternate DNS root
    - ex: https://opennic.org/, https://www.namecoin.org/ 
    - https://en.wikipedia.org/wiki/Alternative_DNS_root
  - dig @[ALTERNATE DNS SERVER IP] [domain] <--- Will give the ip of the domain if found
### Cisco IOS

- username [username] password 7 [password] <--- hashed password is reversable
  - https://packetlife.net/toolbox/type7/ 