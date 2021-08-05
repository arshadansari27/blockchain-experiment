import socket
from app.network.peer_manager import PeerManager
from typing import List
from fastapi import FastAPI
from dataclasses import dataclass, field

from app.network import admin
from app.routers import chain, users

app = FastAPI()

app.include_router(users.router)
app.include_router(chain.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@dataclass
class Config:
    node_id: int = field(init=False)
    init_peer: List[str] = field(init=False)
    peer_manager: PeerManager = field(init=False)
    port: int = field(init=False)
    publish_port: int = field(init=False)
    host: str = field(init=False)

    @staticmethod
    def create_instance(node_id, init_peer):
        global CONFIG

        port = 5000 + node_id
        publish_port = 3000 + node_id
        h_name = socket.gethostname()
        host = f"{socket.gethostbyname(h_name)}:{port}"

        _config = Config()
        _config.node_id = node_id
        _config.init_peer = init_peer
        _config.port = port
        _config.publish_port = publish_port
        _config.peer_manager = PeerManager(host)
        _config.host = host
        CONFIG = _config 
        return CONFIG


CONFIG = None