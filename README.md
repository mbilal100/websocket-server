# Websocket Server

This is a simple websocket server example in Python for communication between multiple clients and a single server application.

## Usage:

```bash
$ python server.py --help 
Usage: server.py [OPTIONS]

Options:
  --port INTEGER  WebSocket port [default: 10000] If unavailable, other ports
                  will be tried
  --help          Show this message and exit.
```

## Example

### Launch server

```bash
$ python server.py --port 1234
Connection address: ws://localhost:1234
```

### Connect with Server

```bash
$ python -m websockets ws://localhost:1234
Connected to ws://localhost:1234.
< Type 'quit' to close the connection
> hello client1
< Received: hello client1
> quit
< Server is closing. Goodbye!
Connection closed.
```

Multiple clients can connect separately. The server will only exit when all client connections are closed.

## Requirements

```bash
$ pip install click websockets
```
