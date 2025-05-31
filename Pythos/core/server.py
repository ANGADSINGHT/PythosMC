# Server socket logic (asyncio, connections)
import asyncio
import time
from Pythos.core import connection

async def handle_client(reader, writer) -> None:
    await connection.handle(reader, writer)

    await writer.drain()
    return writer.close()

async def main(IP: int, PORT: int) -> None:
    start_time = time.perf_counter()
    server = await asyncio.start_server(handle_client, IP, PORT)
    elapsed = time.perf_counter() - start_time
    print(f"Server running on {IP}:{PORT} (started in {elapsed:.4f} seconds)")
    async with server:
        await server.serve_forever()

    return

def start_server(IP: int, PORT: int) -> None:
    return asyncio.run(main(IP, PORT))