from app.network.peer_manager import PeerManager
import sys
import trace
from typing import List
import zmq
from zmq import SUBSCRIBE, SUB
import asyncio
import zmq.asyncio
from zmq.asyncio import Context
import traceback

from zmq.sugar.constants import LINGER


async def start_subscriber(peer_manager: PeerManager):
    context = Context.instance()
    socket = context.socket(SUB)
    try:
        for _peer in peer_manager.peers:
            peer = _peer.strip()
            conn_str = f"tcp://{peer}"
            print(f"={conn_str}=")
            topicfilter = peer.encode('utf8') # peer.encode('utf8')
            socket.setsockopt(SUBSCRIBE, topicfilter)
            socket.bind(conn_str)
        while True:
            string = await socket.recv()
            print(string.decode('utf8'))
    except Exception as _:
        print(traceback.format_exc())
        print("DONE")
    finally:
        socket.setsockopt(LINGER, 0)
        socket.close()


if __name__ == '__main__':
    peers = sys.argv[1:]
    print(peers)
    asyncio.get_event_loop().run_until_complete(
        asyncio.wait([start_subscriber(peers)])
    )
