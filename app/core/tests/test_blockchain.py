import pytest
from ..block import Block
from ..blockchain import Blockchain


@pytest.fixture
def blockchain() -> Blockchain:
    return Blockchain()


@pytest.fixture
def blockchain_2() -> Blockchain:
    return Blockchain()


def test_genesis(blockchain: Blockchain):
    genesis = Block.genesis()
    assert blockchain.chain[0].data == genesis.data
    assert blockchain.chain[0].hash == genesis.hash


def test_add_block(blockchain: Blockchain):
    block = blockchain.add_block('foo')
    assert block.last_hash == blockchain.chain[0].hash


def test_chain_valid(blockchain, blockchain_2):
    blockchain_2.add_block('fooo')
    assert blockchain.is_valid_chain(blockchain_2.chain) is True


def test_chain_invalid(blockchain, blockchain_2):
    blockchain_2.add_block('foo')
    blockchain_2.chain[1].data = 'not foo'
    assert blockchain.is_valid_chain(blockchain_2.chain) is False


def test_replace_chain_with_valid(blockchain, blockchain_2):
    blockchain_2.add_block('goo')
    blockchain.replace_chain(blockchain_2.chain)
    assert blockchain.chain == blockchain_2.chain


def test_replace_chain_invalid_on_less_size(blockchain, blockchain_2):
    blockchain.add_block('shoo')
    blockchain.replace_chain(blockchain_2.chain)
    assert blockchain.chain != blockchain_2.chain


def test_replace_chain_invalid_on_equal_size(blockchain, blockchain_2):
    blockchain.add_block('shoo')
    blockchain_2.add_block('boo')
    blockchain.replace_chain(blockchain_2.chain)
    assert blockchain.chain != blockchain_2.chain
