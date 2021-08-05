import asyncio
import sys
import zmq
import zmq.asyncio
from zmq.asyncio import Context
from zmq.sugar.constants import LINGER


async def start_publisher():
    from app import CONFIG
    from app.routers.chain import blockchain

    context = Context.instance()
    socket = context.socket(zmq.PUB)
    host = CONFIG.host.replace(str(CONFIG.port), str(CONFIG.publish_port))
    conn_str = f"tcp://{host}"
    print(f"PUBLISHER ={conn_str}=")
    socket.bind(conn_str)
    socket.setsockopt(LINGER, 1)
    while True:
        try:
            all_peers = ','.join(CONFIG.peer_manager.peers)
            message = f"peer {all_peers}"
            await socket.send(f"{CONFIG.host} {message}".encode('utf8'))

            size = len(blockchain.chain)
            await socket.send(f"{CONFIG.host} chain {size}".encode('utf8'))

        finally:
            await asyncio.sleep(3)


if __name__ == '__main__':
    port = sys.argv[1]
    asyncio.get_event_loop().run_until_complete(
        asyncio.wait([start_publisher(f"127.0.0.1:{port}", range(100))])
    )
