from Pythos.core.utils.helpers import encode_varint
from Pythos.config.settings import MOTD
import json

async def pong(payload: bytes) -> bytes:
    motd_json = {
        "version": {
            "name": "1.21.5",
            "protocol": 770
        },
        "players": {
            "max": 20,
            "online": 0,
            "sample": []
        },
        "description": {
            "text": MOTD
        }
    }
    motd_str = json.dumps(motd_json, separators=(',', ':')).encode('utf-8')
    packet_id = encode_varint(0x00)
    json_length = encode_varint(len(motd_str))
    packet = packet_id + json_length + motd_str
    packet_length = encode_varint(len(packet))
    return packet_length + packet

async def pong2(payload: bytes) -> bytes:
    response_data = encode_varint(0x01) + payload  # Echo the timestamp
    response_packet = encode_varint(len(response_data)) + response_data
    return response_packet