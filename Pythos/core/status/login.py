from Pythos.core.protocol import read_packet, read_string, build_packet, encode_string
import uuid

async def handle_login(reader, writer) -> str:
    # Step 1: Read login start packet
    packet_id, payload = await read_packet(reader)
    if packet_id != 0x00:
        print("Unexpected packet during login!")
        return

    username, _ = await read_string(payload)
    print(f"Player {username} is logging in")

    # Step 2: Generate fake UUID (offline mode)
    fake_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))  # consistent UUID based on name

    # Step 3: Build Login Success packet
    uuid_bytes = uuid.UUID(fake_uuid).bytes  # 16 raw bytes
    response = build_packet(
        0x02,
        uuid_bytes + encode_string(username)
    )


    writer.write(response)
    return username