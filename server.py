import asyncio
import websockets
import threading
import click
import socket

DEFAULT_START_PORT = 10000
active_connections = set()


def find_port(port, recursive=True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("localhost", port)) == 0:
            if not recursive:
                return None
            return find_port(port=port + 1)
        else:
            return port


async def echo(websocket, path):
    active_connections.add(websocket)
    try:
        await websocket.send("Type 'quit' to close the connection")
        async for message in websocket:
            if message.lower() == 'quit':
                await websocket.send("Server is closing. Goodbye!")
                await websocket.close()  # Close the connection with the client
                break
            else:
                await websocket.send(f"Received: {message}")
    finally:
        active_connections.remove(websocket)

        if not active_connections:
            asyncio.get_event_loop().stop()  # Stop the event loop when all connections are closed


def start_server(port):
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(echo, "localhost", port)
    print("Connection address: ws://localhost:" + str(port))
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


@click.command()
@click.option('--port', type=int,
              help='WebSocket port [default: ' + str(
                  DEFAULT_START_PORT) + '] If unavailable, other ports will be tried')
def main(port):
    # Find free available port
    if port is None:
        port = find_port(DEFAULT_START_PORT)
    # Check if provided port is free
    elif find_port(port) is None:
        raise Exception("The port " + str(self.port) + " is not available for connection")

    # Start the WebSocket server in a separate daemon thread
    server_thread = threading.Thread(target=start_server, args=(port,), daemon=True)
    server_thread.start()

    # Wait for the server thread to finish (which will never happen)
    server_thread.join()


if __name__ == "__main__":
    main()
