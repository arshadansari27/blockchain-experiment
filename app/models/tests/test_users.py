from ..users import User
from . import *


def test_user(db_session):
    user = User(
        username="username-test", password="password-hash", email="test-email"
    )
    user.id = 100
    db_session.add(user)
    db_session.commit()
    assert db_session.query(User).filter(User.id == 100).first() == user
