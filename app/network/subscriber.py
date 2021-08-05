from app.network import load_peers
from aiohttp.client import ClientSession
from app.core.blockchain import Blockchain, Block
from app.network.peer_manager import PeerManager
import sys
from zmq import SUBSCRIBE, SUB
import asyncio
from zmq.asyncio import Context
import traceback
from dateutil import parser

from zmq.sugar.constants import LINGER


async def start_subscriber():
    while True:
        try:
            await listen()
            await asyncio.sleep(3)
        except:
            raise


async def listen():
    from app.routers.chain import blockchain
    from app import CONFIG

    peer_manager = CONFIG.peer_manager
    context = Context.instance()
    socket = context.socket(SUB)
    try:
        curr_subscribe_len = len(peer_manager.subscribed_to_peers)
        if curr_subscribe_len == 0:
            return
        print("Subscription length:", curr_subscribe_len)
        for peer in peer_manager.subscribed_to_peers:
            if peer == peer_manager.self_peer:
                continue
            peer_host = peer.replace('500', '300') # TODO: Dirty hack for port change
            conn_str = f"tcp://{peer_host}"
            print(f"SUBSCRIBER ={conn_str}=")
            topicfilter = peer.encode('utf8') # peer.encode('utf8')
            socket.setsockopt(SUBSCRIBE, topicfilter)
            socket.connect(conn_str)
        while True:
            string = await socket.recv()
            data = string.decode('utf8')
            if 'peer' in data:
                updated_peer = await update_peers(data, peer_manager)
                if updated_peer:
                    break
            elif 'chain' in data:
                await update_chain(data, blockchain)
            else:
                print('\tDo nothing with it')
            new_len = len(peer_manager.subscribed_to_peers)
            if  new_len > curr_subscribe_len:
                break
    except Exception as _:
        print(traceback.format_exc())
        raise
    finally:
        socket.setsockopt(LINGER, 0)
        socket.close()


async def update_peers(data: str, peer_manager: PeerManager):
    _data = data.split()
    latest_peers = _data[2].strip().split(',')
    if peer_manager.update_peers(latest_peers):
        print("\tUpdated peers to ", peer_manager.peers)
        print("\tMight wanna update the connection too?")
        if len(peer_manager.subscribed_to_peers) < 2:
            await load_peers(peer_manager.self_peer, peer_manager)
            return True
    return False


async def update_chain(data: str, blockchain: Blockchain):
    _data = data.split()
    incoming_from = _data[0].strip()
    incoming_size = int(_data[2].strip())
    if len(blockchain.chain) < incoming_size:
        print(f"\tUpdating Chain from {incoming_from}")
        await update_blockchain_from_host(incoming_from, blockchain)


async def update_blockchain_from_host(host: str, blockchain: Blockchain):
    async with ClientSession(trust_env=True) as session:
        async with session.get(
            f'http://{host}/chain'
        ) as response:
            result = await response.json()
            chain = []
            for block in result:
                block['timestamp'] = parser.parse(block['timestamp'])
                chain.append(Block(**block))
            blockchain.replace_chain(chain)



