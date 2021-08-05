from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pytest

from .. import mapper_registry


@pytest.fixture(scope="session")
def db_engine():
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    db_url = "sqlite:///./app/models/tests/test.db"
    engine_ = create_engine(db_url, echo=True)
    mapper_registry.metadata.drop_all(bind=engine_)
    mapper_registry.metadata.create_all(bind=engine_)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()

    yield session_

    session_.close()
