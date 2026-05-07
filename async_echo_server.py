"""Async multi-client TCP echo server with broadcast."""

import asyncio

HOST = "127.0.0.1"
PORT = 9000

clients: list[asyncio.StreamWriter] = []


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr = writer.get_extra_info("peername")
    print(f"[+] Client connected: {addr[0]}:{addr[1]}")
    clients.append(writer)

    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            message = data.decode()
            print(f"    {addr[0]}:{addr[1]} -> {message.strip()}")
            for client in list(clients):
                if client is not writer:
                    try:
                        client.write(data)
                        await client.drain()
                    except ConnectionResetError:
                        pass
    except ConnectionResetError:
        print(f"[!] Client {addr[0]}:{addr[1]} disconnected abruptly")
    finally:
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()
        print(f"[-] Client disconnected: {addr[0]}:{addr[1]}")


async def main() -> None:
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"Async echo server listening on {HOST}:{PORT}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
