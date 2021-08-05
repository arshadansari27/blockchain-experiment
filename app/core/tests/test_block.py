from datetime import datetime
import pytest
from ..block import Block


@pytest.fixture
def last_block():
    return Block.genesis()


@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'bar')


def test_block(block):
    """ Test creation of a simple block """
    assert block.data == 'bar'
    print(block)


def test_block_genesis(last_block):
    """ Test creation of genesis block """
    last_block.hash == 'first_hash'


def test_mining(block):
    new_block = Block.mine_block(block, 'foo')
    assert new_block.data == 'foo'
    assert new_block.last_hash == block.hash


def test_calc_hash():
    hash = Block.calc_hash(datetime.now(), 'test-hash', [])
    print(hash)
    assert len(hash) > 10
