from Pythos.packets.core import read_varint, read_string, write_varint
from json import dumps

async def handshake(writer, resource_state: int, data) -> None:
    print(f"Handshake State: {resource_state}")
    if resource_state == 0:
        offset = 0

        # Packet length (skip)
        _, length_size = read_varint(data, offset)
        offset += length_size

        # Packet ID (should be 0x00)
        packet_id, id_size = read_varint(data, offset)
        offset += id_size

        # Protocol Version
        _, ver_size = read_varint(data, offset)
        offset += ver_size

        # Server Address
        _, addr_size = read_string(data, offset)
        offset += addr_size

        # Port
        offset += 2  # Unsigned short (2 bytes)

        # Next State
        next_state, ns_size = read_varint(data, offset)
        offset += ns_size

        if next_state == 1:
            print("Client wants status")
        elif next_state == 2:
            print("Client wants login")
        else:
            print(f"Unsupported next state: {next_state}")

    elif resource_state == 1:
        # Build the JSON response
        response = {
            "version": {"name": "1.16.5", "protocol": 754},
            "players": {"max": 20, "online": 0},
            "description": {"text": "§aHello from Python Server!"},
        }
        response_json = dumps(response)
        response_bytes = response_json.encode("utf-8")

        # Packet ID = 0x00 for status response
        packet = write_varint(0x00) + write_varint(len(response_bytes)) + response_bytes
        writer.write(write_varint(len(packet)) + packet)
        await writer.drain()
