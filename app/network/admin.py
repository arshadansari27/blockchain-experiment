from app.network.subscriber import start_subscriber
from app.network.publisher import start_publisher
import asyncio
from app.network import load_peers
from fastapi import APIRouter


router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}


@router.post("/register/{addr}")
async def register_peer(addr: str):
    from app import CONFIG

    peer_manager = CONFIG.peer_manager

    peer_manager.update_peers([addr])
    if len(peer_manager.subscribed_to_peers) < 2:
        peer_manager.subscribed_to_peers = [addr]
        print("Updated peer during registration")
    return {
        "message": "Successfuly registered",
        "peers": CONFIG.peer_manager.peers,
    }


@router.get("/connections")
async def get_connections():
    from app import CONFIG

    return {"connections": CONFIG.peer_manager.connected_pairs}


@router.on_event("startup")
async def startup_event():
    from app import CONFIG

    init_peer = CONFIG.init_peer
    peer_manager = CONFIG.peer_manager
    if init_peer:
        await load_peers(init_peer, peer_manager)
    asyncio.get_event_loop().create_task(start_subscriber())
    asyncio.get_event_loop().create_task(start_publisher())
