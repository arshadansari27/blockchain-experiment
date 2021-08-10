from typing import List
from pydantic.main import BaseModel
from fastapi import APIRouter, HTTPException

# from ..dependencies import get_token_header
from app.core.blockchain import Blockchain


class Data(BaseModel):
    transactions: List[str]


router = APIRouter(
    prefix="/chain",
    tags=["chain"],
    responses={404: {"description": "Not found"}},
)
blockchain = Blockchain()


@router.get("/")
async def get_all():
    return blockchain.chain


@router.get("/{hash}")
async def get_block(hash: str):
    response = None
    for block in blockchain.chain:
        if block.hash == hash:
            response = block
            break
    if not response:
        raise HTTPException(status_code=404, detail="Item not found")
    return block


@router.put(
    "/mine",
    tags=["mine"],
    responses={403: {"description": "Operation forbidden"}},
)
async def mine_block(data: Data):
    if not data:
        raise HTTPException(status_code=403, detail="There is no data in body")
    block = blockchain.add_block(data.transactions)
    return block
