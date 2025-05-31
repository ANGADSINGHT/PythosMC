# Utility functions for protocol encoding/decoding

def encode_varint(value):
    result = bytearray()
    while True:
        temp = value & 0x7F
        value >>= 7
        if value:
            result.append(temp | 0x80)
        else:
            result.append(temp)
            break
    return bytes(result)
