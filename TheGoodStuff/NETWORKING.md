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
### Cisco IOS

- username [username] password 7 [password] <--- hashed password is reversable
  - https://packetlife.net/toolbox/type7/ 