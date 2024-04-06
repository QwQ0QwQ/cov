import asyncio
import websockets
import pathlib
import ssl

async def echo(websocket, path):
    async for message in websocket:
        message = "I got your message: {}".format(message)
        await websocket.send(message)

print("webscoket start")
asyncio.get_event_loop().run_until_complete(websockets.serve(echo, 'localhost', 8000))
asyncio.get_event_loop().run_forever()




# async def hello(websocket, path):
#     name = await websocket.recv()
#     print(f"< {name}")
#
#     greeting = f"Hello {name}!"
#
#     await websocket.send(greeting)
#     print(f"> {greeting}")
#
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(
#     pathlib.Path(__file__).with_name('localhost.pem'))
#
# start_server = websockets.serve(
#     hello, 'localhost', 8001, ssl=ssl_context)
#
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

