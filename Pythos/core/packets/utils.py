from asyncio import IncompleteReadError

# --- VarInt helpers ---
async def read_varint(reader):
    num = 0
    for i in range(5):
        if reader.at_eof():
            raise IncompleteReadError(b"", 1)  # Clean failure
        try:
            byte = await reader.readexactly(1)
        except IncompleteReadError:
            raise  # Propagate the error upward
        val = byte[0]
        num |= (val & 0x7F) << (7 * i)
        if not (val & 0x80):
            break
    return num

def write_varint(value):
    out = bytearray()
    while True:
        temp = value & 0x7F
        value >>= 7
        if value:
            out.append(temp | 0x80)
        else:
            out.append(temp)
            break
    return out
