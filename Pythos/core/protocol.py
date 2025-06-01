from Pythos.core.utils.helpers import encode_varint
import Pythos.core.status.pong as pong
from nbtlib import File, Compound
from io import BytesIO

PACKET_FUNCTIONS = {
    0x00: pong.pong,   # Status request (MOTD)
    0x01: pong.pong2  # Ping request (Pong)
}

async def read_varint(reader):
    num = 0
    for i in range(5):  # VarInt is at most 5 bytes
        byte = await reader.read(1)
        if not byte:
            raise ConnectionError("Socket closed while reading VarInt")
        val = byte[0]
        num |= (val & 0x7F) << (7 * i)
        if not (val & 0x80):
            break
    return num

async def read_varint_from_bytes(data, offset):
    num = 0
    bytes_read = 0
    for i in range(5):
        val = data[offset + i]
        num |= (val & 0x7F) << (7 * i)
        bytes_read += 1
        if not (val & 0x80):
            break
    return num, bytes_read

async def read_packet(reader):
    length = await read_varint(reader)
    packet_id = await read_varint(reader)
    payload = await reader.read(length - len(encode_varint(packet_id)))
    return packet_id, payload

async def handle_packet(packet_id, payload) -> bytes | None:
    if packet_id in PACKET_FUNCTIONS:
        return await PACKET_FUNCTIONS[packet_id](payload)
    
    return None

def encode_string(s: str) -> bytes:
    encoded = s.encode('utf-8')
    return encode_varint(len(encoded)) + encoded

async def read_string(data: bytes, offset=0):
    length, n = await read_varint_from_bytes(data, offset)
    offset += n
    string_bytes = data[offset:offset+length]
    return string_bytes.decode('utf-8'), offset + length

def build_packet(packet_id: int, payload: bytes) -> bytes:
    packet_id_bytes = encode_varint(packet_id)
    packet = packet_id_bytes + payload
    return encode_varint(len(packet)) + packet

def encode_nbt(nbt_file):
    buffer = BytesIO()
    nbt_file.write(buffer)
    return buffer.getvalue()


