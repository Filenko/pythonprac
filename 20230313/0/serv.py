import asyncio


async def echo(reader, writer):
    while not reader.at_eof():
        data = await reader.readline()
        match data.decode().split(maxsplit=1):
            case ["print", str]:
                writer.write(str.encode())
            case ["info", "host\n"]:
                host = writer.get_extra_info('peername')[0]
                writer.write(f"{host}\n".encode())
            case ["info", "port\n"]:
                port = writer.get_extra_info('peername')[1]
                writer.write(f"{port}\n".encode())


    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())

