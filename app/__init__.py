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


CONFIG = Config()