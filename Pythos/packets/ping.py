async def ping(writer) -> None:
    payload = data[offset:]  # 8 bytes
    # Echo the same payload back
    packet = write_varint(0x01) + payload
    writer.write(write_varint(len(packet)) + packet)
    await writer.drain()