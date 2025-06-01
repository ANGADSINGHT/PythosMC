import asyncio
from Pythos.config import IP, PORT
from Pythos.core.packets.PacketHandler import HandlePacket

async def handle_client(reader, writer):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            
            await HandlePacket(reader, writer)
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, IP, PORT)
    async with server:
        print(f"Server is running on {IP}:{PORT}")
        await server.serve_forever()

def start():
    asyncio.run(main())
    print(2)
