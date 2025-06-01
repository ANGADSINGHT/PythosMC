def read_varint(data: bytes, offset=0):
    num_read = 0
    result = 0

    while True:
        if offset + num_read >= len(data):
            raise ValueError("Incomplete VarInt")

        byte = data[offset + num_read]
        result |= (byte & 0x7F) << (7 * num_read)

        num_read += 1
        if num_read > 5:
            raise ValueError("VarInt is too big")

        if (byte & 0x80) == 0:
            break

    return result, num_read

def read_string(data: bytes, offset=0):
    str_len, len_size = read_varint(data, offset)
    start = offset + len_size
    end = start + str_len

    if end > len(data):
        raise ValueError("Incomplete string data")

    string = data[start:end].decode("utf-8")
    return string, len_size + str_len

def write_varint(value: int) -> bytes:
    """Encodes an integer into VarInt format (used by Minecraft protocol)."""
    result = bytearray()
    value &= 0xFFFFFFFF  # Ensure it's within 32-bit unsigned range

    while True:
        byte = value & 0x7F
        value >>= 7
        if value != 0:
            byte |= 0x80
        result.append(byte)
        if value == 0:
            break

    return bytes(result)
