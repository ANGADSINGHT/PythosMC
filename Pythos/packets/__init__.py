from Pythos.packets.handshake import handshake
from Pythos.packets.ping import ping

def read_varint(data: bytes):
    num = 0
    shift = 0
    for i, byte in enumerate(data):
        num |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            return num, i + 1
        shift += 7
    raise ValueError("VarInt too long")

def write_varint(value: int):
    bytes_ = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            byte |= 0x80
        bytes_.append(byte)
        if not value:
            break
    return bytes_