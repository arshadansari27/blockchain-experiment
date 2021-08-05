import asyncio
import sys
import zmq
import zmq.asyncio
from zmq.asyncio import Context
from zmq.sugar.constants import LINGER


async def start_publisher(self_peer, messages):
    context = Context.instance()
    socket = context.socket(zmq.PUB)
    conn_str = f"tcp://{self_peer}"
    print(f"={conn_str}=")
    socket.connect(conn_str)
    socket.setsockopt(LINGER, 1)

    for message in messages:
        print("Sending", message)
        await socket.send(f"{self_peer} {message}".encode('utf8'))
        await asyncio.sleep(1)


if __name__ == '__main__':
    port = sys.argv[1]
    asyncio.get_event_loop().run_until_complete(
        asyncio.wait([start_publisher(f"127.0.0.1:{port}", range(100))])
    )
