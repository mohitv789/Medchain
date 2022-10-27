import os
from django.shortcuts import render
import requests
from medchain.blockchain import Medchain

from .pubsub import PubSub

blockchain = Medchain()
pubsub = PubSub(blockchain)
if os.environ.get('PEER') == "True":
    result = requests.get('http://localhost:8000/blockchain')
    result_blockchain = Medchain.from_json(result.json())
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('\n -- Successfully synchronized the local chain')
    except Exception as e:
        print(f'\n -- Error synchronizing: {e}')

def home(request):
    return render(request,'medchain/home.html')

def get_blockchain(request):
    return render(request,'medchain/blockchain.html',{'medchain': blockchain})

def mine_block(request):    
    transaction_data = "stubbed transaction data"
    blockchain.add_block(transaction_data)
    mined_block = blockchain.chain[-1] 
    pubsub.broadcast_block(mined_block)
    return render(request,'medchain/mine.html',{'mined_block': mined_block})


