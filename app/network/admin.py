from app.network.peer_manager import PeerManager
from typing import List
from fastapi import APIRouter
import requests


router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}


@router.post("/register/{addr}")
async def register_peer(addr: str):
    from app import CONFIG

    CONFIG.peer_manager.update_peers([addr])
    await broadcast_peer()
    return {
        'message': 'Successfuly registered',
        'peers': CONFIG.peer_manager.peers
    }


@router.post("/connections")
async def get_connections():
    from app import CONFIG

    return {
        'connections': CONFIG.peer_manager.connected_pairs
    }


@router.on_event("startup")
async def startup_event():
    from app import CONFIG

    init_peer = CONFIG.init_peer
    peer_manager = CONFIG.peer_manager
    if init_peer:
        await load_peers(init_peer, peer_manager)


async def load_peers(init_peer: str, peer_manager: PeerManager):
    response = requests.post(
        f'http://{init_peer}/admin/register/{peer_manager.self_peer}'
    )
    result = response.json()
    peer_manager.update_peers(result['peers'])
    connections = []
    for peer in result['peers']:
        response = requests.post(f'http://{peer}/admin/connections')
        result = response.json()
        for connected_peer in result['connections']:
            connections.append(tuple([peer, connected_peer]))
    peer_manager.update_connection(connections)
    subscribe_to = peer_manager.choose_peers_to_connect()
    await init_subscription(subscribe_to)


async def init_subscription(subscribe_to: List[str]):
    pass


async def broadcast_peer():
    pass
