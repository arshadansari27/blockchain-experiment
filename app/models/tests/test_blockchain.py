from datetime import datetime

from sqlalchemy.orm.session import Session
from . import *
from ..users import User
from ..blockchain import Block, Transaction


def test_block_chain(db_session: Session):
    with db_session.no_autoflush:
        user_1 = User(
            username="test_user_1", password="", email="test_user_1_email"
        )
        user_2 = User(
            username="test_user_2", password="", email="test_user_2_email"
        )
        db_session.add(user_1)
        db_session.add(user_2)
        db_session.commit()
        block = Block(datetime.now(), 100, "test-hash")
        db_session.add(block)
        db_session.commit()
        transaction_1 = Transaction(10, datetime.now())
        transaction_1.block = block
        transaction_1.sender = user_1
        transaction_1.recipient = user_2
        block.transactions.append(transaction_1)
        transaction_2 = Transaction(1, datetime.now())
        transaction_2.block = block
        transaction_2.sender = user_2
        transaction_2.recipient = user_1
        block.transactions.append(transaction_2)
        transaction_3 = Transaction(9, datetime.now())
        transaction_3.block = block
        transaction_3.sender = user_2
        transaction_3.recipient = user_1
        block.transactions.append(transaction_2)
        db_session.add(block)
        db_session.commit()

        block = db_session.query(Block).first()
        assert block is not None
        for transaction in block.transactions:
            assert transaction.sender.id in {user_1.id, user_2.id}
            assert transaction.recipient.id in {user_1.id, user_2.id}
