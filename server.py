import asyncio

Host = "127.0.0.1"
Port = 9000

clients = set()

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[CONNECTED] {addr}")
    clients.add(writer)

    try:

        read_task = asyncio.create_task(client_read(reader, writer, addr))
        write_task = asyncio.create_task(client_write(writer, addr))


        await read_task
        write_task.cancel()
    except Exception as e:
        print(f"[ERROR] {addr} -> {e}")
    finally:
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

        print(f"[DISCONNECTED] {addr}")

async def client_read(reader, writer, addr):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        
        message = data.decode().strip()

        print(message)

        await broadcast(message, writer)

async def client_write(writer, addr):
    while True:
        await asyncio.sleep(4)
        message = "Server Test Message Periodic"
        writer.write(message.encode())
        await writer.drain()

async def broadcast(message, sender_writer):
    for client in clients:
        if client != sender_writer:
            client.write(message.encode())
            await client.drain()
        

async def start_server():

    server = await asyncio.start_server(handle_client, Host, Port)
    print("server started")
    async with server:
        await server.serve_forever()

asyncio.run(start_server())
