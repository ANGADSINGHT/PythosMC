from Pythos.core.protocol import read_packet, handle_packet

async def handle(reader, writer) -> None:
    packet_id, payload = await read_packet(reader)

    response = await handle_packet(packet_id, payload)
    if response is None:
        return print(f"Unhandled packet with ID: {packet_id:#02x}")


    writer.write(response)
    await writer.drain()
