from json import dumps

async def handshake(writer, data, resource_state: int) -> None:
    if resource_state == 0:
        # Just get the next state (at end of packet)
        # We're skipping version/hostname/port parsing here
        next_state = data[-1]
        if next_state == 1:
            print("Client wants status")
        else:
            print("Unsupported next state")
    elif resource_state == 1:
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
