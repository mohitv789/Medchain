from django.test import TestCase
import time

from numpy import block
from medchain.views import GENESIS_DATA, Block, Medchain
from .config import MINE_RATE,SECONDS
from .helper import crypto_hash, hex_to_binary
import pytest

class MedchainTest(TestCase):

    def test_crypto_hash(self):
        assert crypto_hash(1,[2],"three") == crypto_hash("three",1,[2])

    def test_mine_block(self):
        last_block = Block.genesis()
        data = 'test-data'
        block = Block.mine_block(last_block,data)
        assert isinstance(block,Block)
        assert block.data == data
        assert block.last_hash==last_block.hash
        assert hex_to_binary(block.hash)[0:block.difficulty] == '0'*block.difficulty

    def test_genesis(self):
        genesis = Block.genesis()

        assert isinstance(genesis,Block)
        for key,value in GENESIS_DATA.items():
            getattr(genesis,key) == value
    
    def test_blockchain(self):
        blockchain = Medchain()
        assert blockchain.chain[0].hash==GENESIS_DATA['hash']
    
    def test_add_block(self):
        blockchain = Medchain()
        data='test-data'
        blockchain.add_block(data)
        assert blockchain.chain[-1].data == data
    
    def test_quickly_mined_block(self):
        last_block = Block.mine_block(Block.genesis(),"foo")
        mined_block = Block.mine_block(last_block,'bar')
        assert mined_block.difficulty == last_block.difficulty + 1

    def test_slowly_mined_block(self):
        last_block = Block.mine_block(Block.genesis(),"foo")
        time.sleep(MINE_RATE / SECONDS)
        mined_block = Block.mine_block(last_block,'bar')
        assert mined_block.difficulty == last_block.difficulty - 1

    def test_mined_block_difficulty_limits_at_1(self):
        last_block = Block(
            time.time_ns(),
            "test_last_hash",
            "test_hash",
            "test_data",
            1,
            0
        )
        time.sleep(MINE_RATE / SECONDS)
        mined_block = Block.mine_block(last_block,'bar')
        assert mined_block.difficulty == 1

    def test_hex_to_binary(self):
        original_number = 789
        hex_number = hex(original_number)[2:]
        binary_number = hex_to_binary(hex_number)
        assert int(binary_number,2) == original_number

    def test_is_valid_block(self):
        last_block = Block.genesis()
        block = Block.mine_block(last_block,"test data")
        Block.is_valid_block(last_block,block)

    def test_is_valid_block_bad_Last_hash(self):
        last_block = Block.genesis()
        block = Block.mine_block(last_block,"test data")
        block.last_hash = "evil_last_hash"
        with pytest.raises(Exception,match="The block last_hash must be correct"):
            Block.is_valid_block(last_block,block)

    def test_is_valid_block_bad_proof_of_work(self):
        last_block = Block.genesis()
        block = Block.mine_block(last_block,"test data")
        block.hash = "fff"        
        with pytest.raises(Exception,match="The proof of work requirement was not met"):
            Block.is_valid_block(last_block,block)
    
    def test_is_valid_block_jumped_difficulty(self):
        last_block = Block.genesis()
        block = Block.mine_block(last_block,"test data")
        block.difficulty = 10
        block.hash = f'{"0"*10}111abc'
        with pytest.raises(Exception,match="The block difficulty must only be adjusted by 1"):
            Block.is_valid_block(last_block,block)

    def test_is_valid_block_bad_block_hash(self):
        last_block = Block.genesis()
        block = Block.mine_block(last_block,"test data")
        block.hash = "000000000000aabbcc"        
        with pytest.raises(Exception,match="The block hash must be correct"):
            Block.is_valid_block(last_block,block)

    def test_is_valid_chain(self):
        blockchain = Medchain()
        for i in range(3):
            blockchain.add_block(i)
        Medchain.is_valid_chain(blockchain.chain)

    def test_is_valid_chain_bad_genesis_block(self):
        blockchain = Medchain()
        for i in range(3):
            blockchain.add_block(i)
        blockchain.chain[0].hash = "evil hash"
        with pytest.raises(Exception,match="The genesis block must be valid"):
            Medchain.is_valid_chain(blockchain.chain)
    
    def test_replace_chain(self):
        old_blockchain = Medchain()
        for i in range(3):
            old_blockchain.add_block(i)
        new_blockchain = Medchain()
        new_blockchain.replace_chain(old_blockchain.chain)
        assert new_blockchain.chain == old_blockchain.chain

    def test_replace_chain_not_longer(self):
        old_blockchain = Medchain()
        for i in range(3):
            old_blockchain.add_block(i)
        new_blockchain = Medchain()
        with pytest.raises(Exception,match="Cannot replace. The incoming chain must be longer"):
            old_blockchain.replace_chain(new_blockchain.chain)

    def test_replace_chain_bad_chain(self):
        old_blockchain = Medchain()
        for i in range(3):
            old_blockchain.add_block(i)
        old_blockchain.chain[1].hash = "evil hash"
        new_blockchain = Medchain()
        with pytest.raises(Exception,match="Cannot replace. The incoming chain is invalid"):
            new_blockchain.replace_chain(old_blockchain.chain)
        

