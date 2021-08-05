import sqlalchemy

from sqlalchemy.orm import registry
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker


DATABASE_URL = "sqlite:///./blockchain.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

mapper_registry = registry()

from .users import User
from .blockchain import *

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
mapper_registry.metadata.create_all(bind=engine)
_session = scoped_session(sessionmaker(bind=engine))
with _session() as _session_object:
    node_user = _session_object.query(User).filter(User.id == 1).first()
    if not node_user:
        node_user = User(
            username="node",
            password="kkkkkkkkasssasdfasdf",
            email="admin@blocky",
        )
        _session_object.add(node_user)
        _session_object.commit()
    node_user = _session_object.query(User).filter(User.id == 1).first()
    assert node_user is not None


__all__ = [User, Block, Transaction, node_user]
