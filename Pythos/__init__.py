import asyncio

async def handle_client(reader, writer):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            
            # Server logic
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 25565)
    async with server:
        print("Server is running")
        await server.serve_forever()

def start():
    asyncio.run(main())
