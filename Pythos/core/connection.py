from Pythos.core.protocol import read_packet, handle_packet, read_varint_from_bytes
from Pythos.core.status.login import handle_login
from Pythos.core.play.join_game import minimal_join_game_packet

async def parse_handshake(payload: bytes):
    i = 0
    # Skip protocol version
    _, n = await read_varint_from_bytes(payload, i)
    i += n
    # Skip server address (MC string: varint length + bytes)
    addr_len, n = await read_varint_from_bytes(payload, i)
    i += n + addr_len
    # Skip port (2 bytes)
    i += 2
    # Next state
    next_state, _ = await read_varint_from_bytes(payload, i)
    return next_state

async def handle(reader, writer) -> None:
    # Step 1: Read handshake packet
    packet_id, payload = await read_packet(reader)
    if packet_id == 0x00:  # Handshake
        next_state = await parse_handshake(payload)
        if next_state == 1:  # Status
            # Step 2: Read status request packet
            packet_id, payload = await read_packet(reader)

            status_response = await handle_packet(packet_id, payload)
            if status_response:
                writer.write(status_response)
                await writer.drain()

            # Step 3: Read ping packet
            packet_id, payload = await read_packet(reader)
            if packet_id == 0x01:
                pong_response = await handle_packet(packet_id, payload)
                if pong_response:
                    writer.write(pong_response)
                    await writer.drain()

        elif next_state == 2:  # Login
            # Handle login and send Join Game/world config packet
            await handle_login(reader, writer)
            join_game_packet = await minimal_join_game_packet(1)            
            writer.write(join_game_packet)
            await writer.drain()
            print("Sent join game packet")
    return

