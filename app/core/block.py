from datetime import datetime
from typing import Any, List
import hashlib


class Block:
    def __init__(self, timestamp: datetime, last_hash: str, hash: str, data: List[Any]) -> None:
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data

    def __repr__(self) -> str:
        return f"""Block - 
    Timestamp: {self.timestamp}
    Last Hash: {self.last_hash[:10] if self.last_hash else None}
    Hash: {self.hash[:10] if self.hash else None}\n"""

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
        return Block(datetime(1970, 1, 1), None, 'first_hash', [])

    @staticmethod
    def mine_block(last_block: "Block", data: List[Any]):
        timestamp = datetime.now()
        last_hash = last_block.hash
        hash = Block.calc_hash(timestamp, last_hash, data)
        return Block(timestamp, last_hash, hash, data)

    @staticmethod
    def calc_hash(timestamp: datetime, last_hash: str, data: List[Any]):
        #block_string = json.dumps(asdict(self), sort_keys=True).encode()
        block_string = f"{timestamp.strftime('%Y%m%d%H%M%S')}-{last_hash}-{':'.join(data)}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    @staticmethod
    def calc_hash_from_block(block: "Block"):
        return Block.calc_hash(block.timestamp, block.last_hash, block.data)
