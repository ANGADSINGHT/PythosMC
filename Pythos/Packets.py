from Pythos.packets import *

PACKET_FUNCTIONS = {
    0x00:handshake
}

async def handlePacket(data, writer) -> None:
    packet_len, offset = read_varint(data)
    packet_id, id_len = read_varint(data[offset:])
    offset += id_len
    
    if packet_id not in PACKET_FUNCTIONS:
        return print(f"Packet unhandled with ID: {packet_id}")

    # Handshake Packet
    if packet_id == 0x00:
        print("Sending handshake packet...")
        await PACKET_FUNCTIONS[packet_id](writer, 0, data)

    # Status Request
    elif packet_id == 0x00:  # Status request
        print("Sending status packet...")
        await PACKET_FUNCTIONS[packet_id](writer, 1, data)

    # Ping Packet
    elif packet_id == 0x01:
        print("Sending ping packet...")
        await PACKET_FUNCTIONS[packet_id](writer)