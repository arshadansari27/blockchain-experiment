import asyncio
from datetime import datetime

from app.core.blockchain import Blockchain
from app.core.block import Block
from fastapi import WebSocket
from typing import Dict, List, Optional
from pydantic import BaseModel
from .peer_manager import PeerManager


class MessageDTO(BaseModel):
    type: str


class PeerDTO(MessageDTO):
    peers: List[str]


class ChainDTO(MessageDTO):
    chain: List["BlockDTO"]

    def to_model(self):
        bchain = Blockchain()
        bchain.chain = [
            Block(
                timestamp=block_dto.timestamp,
                hash=block_dto.hash,
                last_hash=block_dto.last_hash,
                data=block_dto.data,
            )
            for block_dto in self.chain
        ]
        return bchain

    @staticmethod
    def to_dto(blockchain: Blockchain):
        chains = [
            BlockDTO(
                timestamp=block.timestamp,
                hash=block.hash,
                last_hash=block.last_hash,
                data=block.data,
            )
            for block in blockchain.chain
        ]
        dto = ChainDTO(
            chain=chains,
            type='chain',
        )
        return dto


class BlockDTO(BaseModel):
    timestamp: datetime
    hash: str
    data: Optional[List[str]] = []
    last_hash: Optional[str] = None


async def broadcast_update(blockchain: Blockchain):
    message_dto = ChainDTO.to_dto(blockchain)


async def broadcast_peers(peer: List[str]):
    pass


async def handle_client_connection(blockchain: Blockchain):
    pass