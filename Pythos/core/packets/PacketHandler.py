from Pythos.core.packets.utils import read_varint
from Pythos.core.packets.status.handshake import handshake

async def HandlePacket(reader, writer) -> None:
    # Step 1: Read Packet Length and ID
    packet_length = await read_varint(reader)
    packet_id = await read_varint(reader)

    print(f"---------NEW PACKET--------\nID: {packet_id}")
    if packet_id == 0x00:  # Handshake
        await handshake(reader, writer)

    return