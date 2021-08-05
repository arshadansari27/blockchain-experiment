import json
import hashlib
from copy import copy
from dataclasses import asdict, dataclass, field
from datetime import datetime
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    ForeignKey,
    TIMESTAMP,
    Float,
)
from sqlalchemy.orm import relationship, Session
from typing import Optional, List

from sqlalchemy.sql.expression import asc, desc

from . import mapper_registry
from .users import User


CHAIN = None


@mapper_registry.mapped
@dataclass
class Block:
    __table__ = Table(
        "block",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("timestamp", TIMESTAMP(), nullable=False),
        Column("proof", Integer, nullable=False),
        Column("previous_hash", String(500), nullable=False),
    )
    id: int = field(init=False)
    timestamp: Optional[datetime] = None
    proof: Optional[int] = None
    previous_hash: Optional[str] = None
    transactions: List["Transaction"] = field(default_factory=list)

    __mapper_args__ = {
        "properties": {
            "transactions": relationship("Transaction", back_populates="block"),
        }
    }

    def hash(self):
        block_string = json.dumps(asdict(self), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def new_block(
        session: Session, proof: int, previous_hash: str = None
    ) -> "Block":
        last_block = (
            session.query(Block).order_by(desc(Block.timestamp)).first()
        )
        block = Block(
            timestamp=datetime.now(),
            proof=proof,
            previous_hash=previous_hash or hash(asdict(last_block)),
        )
        session.add(block)
        return block

    @staticmethod
    def build_chain(session: Session) -> None:
        global CHAIN
        blocks = list(session.query(Block).order_by(asc(Block.timestamp)).all())
        size = len(blocks)
        if not blocks:
            first_block = Block.new_block(session, 0, None)
            session.add(first_block)
            session.commit()
            blocks.append(first_block)
        for idx, block in enumerate(blocks):
            if idx < (size - 1):
                jdx = idx + 1
                assert block.hash() == blocks[jdx].previous_hash
        session.expunge_all()
        CHAIN = [b for b in block]


@mapper_registry.mapped
@dataclass
class Transaction:
    __table__ = Table(
        "transaction",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column(
            "block_id",
            Integer,
            ForeignKey("block.id", name="fk_block_id"),
            nullable=False,
        ),
        Column(
            "sender_id",
            String(500),
            ForeignKey("user.id", name="fk_trans_s_id"),
            nullable=False,
        ),
        Column(
            "recipient_id",
            String(500),
            ForeignKey("user.id", name="fk_trans_r_id"),
            nullable=False,
        ),
        Column("amount", Float(500), nullable=False),
        Column("timestamp", TIMESTAMP(), nullable=False),
    )
    id: int = field(init=False)
    block_id: int = field(init=False)
    sender_id: int = field(init=False)
    recipient_id: int = field(init=False)
    amount: float
    timestamp: datetime
    sender: User = field(init=False)
    recipient: User = field(init=False)
    block: Block = field(init=False)

    __mapper_args__ = {
        "properties": {
            "sender": relationship(
                "User",
                back_populates="sent_transactions",
                primaryjoin="User.id == Transaction.sender_id",
            ),
            "recipient": relationship(
                "User",
                back_populates="recieved_transactions",
                primaryjoin="User.id == Transaction.recipient_id",
            ),
            "block": relationship("Block", back_populates="transactions"),
        }
    }

    @staticmethod
    def new_transaction(
        session: Session, sender: User, recipient: User, amount: float
    ) -> "Transaction":
        if isinstance(amount, str):
            amount = float(amount)
        current_block = (
            session.query(Block).order_by(desc(Block.timestamp)).first()
        )
        transaction = Transaction(
            sender=sender, recipient=recipient, amount=amount
        )
        current_block.transactions.append(transaction)
        session.add(current_block)
        return transaction.id
