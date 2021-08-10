from datetime import datetime, timedelta
from typing import Any, List
import hashlib


DIFFICULTY = 2
MINE_CTRL = 30


class Block:
    def __init__(
        self,
        timestamp: datetime,
        last_hash: str,
        hash: str,
        data: List[Any],
        difficulty: int,
        nonce: int,
    ) -> None:
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self) -> str:
        return f"""Block - 
    Timestamp  : {self.timestamp}
    Last Hash  : {self.last_hash[:10] if self.last_hash else None}
    Difficulty : {self.difficulty}
    Nonce      : {self.nonce}
    Hash       : {self.hash[:10] if self.hash else None}\n"""

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Block):
            return False
        if o.timestamp is not None and self.timestamp is not None:
            if o.timestamp != self.timestamp:
                return False
        if o.last_hash is not None and self.last_hash is not None:
            if o.last_hash != self.last_hash:
                return False
        if o.hash is not None and self.hash is not None:
            if o.hash != self.hash:
                return False
        if o.data is not None and self.data is not None:
            if o.data != self.data:
                return False
        return True

    @staticmethod
    def genesis() -> "Block":
        return Block(
            datetime(1970, 1, 1), None, "first_hash", [], DIFFICULTY, 0
        )

    @staticmethod
    def mine_block(last_block: "Block", data: List[Any]):
        last_hash = last_block.hash
        nonce = 0
        difficulty = last_block.difficulty
        while True:
            nonce += 1
            timestamp = datetime.now()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = Block.calc_hash(
                timestamp, last_hash, data, difficulty, nonce
            )
            if hash[:difficulty] == ("0" * difficulty):
                break
        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def calc_hash(
        timestamp: datetime,
        last_hash: str,
        data: List[Any],
        difficulty: int,
        nonce: int,
    ):
        ts = timestamp.strftime("%Y%m%d%H%M%S")
        dt = ":".join(data)
        block_string = f"{ts}{last_hash}{dt}{difficulty}{nonce}"
        return hashlib.sha256(block_string.encode("utf-8")).hexdigest()

    @staticmethod
    def calc_hash_from_block(block: "Block"):
        return Block.calc_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce,
        )

    @staticmethod
    def adjust_difficulty(last_block: "Block", timestamp: datetime):
        difficulty = last_block.difficulty
        if timestamp + timedelta(seconds=MINE_CTRL) > datetime.now():
            difficulty += 1
        else:
            difficulty -= 1
        return difficulty
