from Pythos.core.packets.utils import read_varint, write_varint
from json import dumps
from asyncio import IncompleteReadError

async def handle_status(reader, writer):
    try:
        print("Handling status...")
        # Step 1: Read status request packet
        packet_len = await read_varint(reader)
        packet_id = await read_varint(reader)
        if packet_id != 0x00:
            print("Unexpected packet ID during status:", packet_id)
            return

        # Step 2: Build status JSON
        status = {
            "version": {"name": "1.16.5", "protocol": 754},
            "players": {
                "max": 20,
                "online": 5,
                "sample": [{"name": "Steve", "id": "00000000-0000-0000-0000-000000000000"}]
            },
            "description": {"text": "Hello from Python!"},
        }
        json_bytes = dumps(status).encode("utf-8")

        # Step 3: Create packet
        packet_id = write_varint(0x00)                # Status Response packet ID
        json_len = write_varint(len(json_bytes))      # Length of JSON
        data = packet_id + json_len + json_bytes      # [ID][len][json]

        # Step 4: Prepend total length
        total_len = write_varint(len(data)) + data    # [packet length][packet data]

        writer.write(total_len)
        await writer.drain()

        # Step 5: Handle ping (optional)
        packet_len = await read_varint(reader)
        packet_id = await read_varint(reader)
        if packet_id == 0x01:
            payload = await reader.readexactly(8)  # long (8 bytes)
            pong = write_varint(0x01) + payload
            writer.write(write_varint(len(pong)) + pong)
            await writer.drain()

        print("Handled status?")
    except Exception as e:
        print("Status handler error:", e)



async def handshake(reader, writer) -> None:
    print("Handshaking Packet!")
    try:
        # Read protocol version
        _ = await read_varint(reader)  # protocol version
        # Read server address
        host_len = await read_varint(reader)
        host = (await reader.readexactly(host_len)).decode()
        port = int.from_bytes(await reader.readexactly(2), "big")
        next_state = await read_varint(reader)
        print("Next State: ", next_state)

        if next_state == 1:
            # Expecting status request next
            await handle_status(reader, writer)
    except IncompleteReadError:
        print("Client disconnected during handshake (IncompleteReadError)")
        return