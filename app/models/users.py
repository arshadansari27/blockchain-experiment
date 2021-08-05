from dataclasses import dataclass, field
from sqlalchemy import Table, Column, String, Integer
from sqlalchemy.orm import relationship, Session
from typing import Optional, List


from . import mapper_registry


@mapper_registry.mapped
@dataclass
class User:
    __table__ = Table(
        "user",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("username", String(80), unique=True, nullable=False),
        Column("email", String(120), unique=True, nullable=False),
        Column("password", String(80), nullable=False),
    )
    id: int = field(init=False)
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    sent_transactions: List["Transaction"] = field(default_factory=list)
    recieved_transactions: List["Transaction"] = field(default_factory=list)

    __mapper_args__ = {
        "properties": {
            "sent_transactions": relationship(
                "Transaction",
                back_populates="sender",
                primaryjoin="User.id == Transaction.sender_id",
            ),
            "recieved_transactions": relationship(
                "Transaction",
                back_populates="recipient",
                primaryjoin="User.id == Transaction.recipient_id",
            ),
        }
    }

    @staticmethod
    def create_node_user(session: Session):
        node_user = session.query(User).filter(User.id == 1).first()
        if not node_user:
            node_user = User(
                username="node",
                email="s@b.com",
                password="asdlfjasdflaksjfdsfjalfjdalkfjasf",
            )
            node_user.id = 1
            session.add(node_user)

    @staticmethod
    def get_by_id(session: Session, id: int):
        return session.query(User).filter(User.id == id).first()
