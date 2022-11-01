
import requests
import blockchain
from medchain.block import Block
from urllib.parse import urlparse

class Medchain():

    def __init__(self):
        self.chain = [Block.genesis()]
    
    def add_block(self,data):
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block,data))

    def __repr__(self):
        return f'Medchain: {self.chain}'


    def replace_chain(self,chain):        
        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace. The incoming chain must be longer.")
        try:
            Medchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f"Cannot replace. The incoming chain is invalid: {e}")
        self.chain = chain

    def to_json(self):
        serlialized_chain = []
        for block in self.chain:
            serlialized_chain.append(block.to_json())
        return serlialized_chain

    @staticmethod
    def from_json(chain_json):
        blockchain = Medchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json),chain_json))
        return blockchain
        
    @staticmethod
    def is_valid_chain(chain):

        if chain[0]!=Block.genesis():
            raise Exception("The genesis block must be valid")

        for i in range(1,len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block,block)

    def get_block(self,ts):
        for item in self.chain:
            if item.timestamp == ts:
                return item
