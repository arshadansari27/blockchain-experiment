from typing import Any, List
from .block import Block


class Blockchain:
    def __init__(self) -> None:
        self.chain = [Block.genesis()]

    def add_block(self, data: List[Any]) -> Block:
        block = Block.mine_block(self.chain[-1], data)
        self.chain.append(block)
        return block

    def is_valid_chain(self, chain: List[Block]) -> bool:
        if not (self.chain[0] == Block.genesis()):
            return False
        for i, block in enumerate(chain[1:]):
            last_block = chain[i]
            if block.last_hash != last_block.hash:
                return False
            if block.hash != Block.calc_hash_from_block(block):
                return False
        return True

    def __repr__(self) -> str:
        return f"Block chain (length = {len(self.chain)})"

    def replace_chain(self, chain: List[Block]) -> None:
        if len(chain) <= len(self.chain):
            print("[*] Recieved chain is not longer than current")
        elif not self.is_valid_chain(chain):
            print("[*] Recieved chain is not valid")
        else:
            print("[*] Replacing new chain")
            self.chain = chain
