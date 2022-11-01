from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from medchain.forms import TransactionForm
from medchain.blockchain import Medchain
from medchain.transaction import Transaction
from medchain.transaction_pool import TransactionPool
from medchain.wallet import Wallet
from .pubsub import PubSub
import json

blockchain = Medchain()
wallet = Wallet()
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain,transaction_pool)


def home(request):
    return render(request,'medchain/home.html')

def get_blockchain(request):
    # Maybe try to add call to all nodes here
    return render(request,'medchain/blockchain.html',{'medchain': blockchain})

def get_block_data(request,ts):
    block = blockchain.get_block(ts)
    print(block)
    return render(request,'medchain/block.html',{'block': block})

def mine_block(request):    
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    mined_block = blockchain.chain[-1]
    pubsub.broadcast_block(mined_block)
    transaction_pool.clear_blockchain_transactions(blockchain)
    return render(request,'medchain/mine.html',{'mined_block': mined_block})

def commit_wallet_transact(request):
    template_name = "medchain/commit_transaction.html"
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        transaction_data = {}
        transaction_data['recipient'] = request.POST['recipient']
        transaction_data['amount'] = request.POST['amount']
        transaction = transaction_pool.existing_transaction(wallet.address)

        if transaction:
            transaction.update(
                wallet,
                transaction_data['recipient'],
                transaction_data['amount']
            )
            
            print('Transaction Object:  {transaction}')
        else:
            transaction = Transaction(
                wallet,
                transaction_data['recipient'],
                transaction_data['amount']
            )
            
            print('Transaction Object:  {transaction}')

        pubsub.broadcast_transaction(transaction)
        request.session['transaction'] = transaction.to_json()
        return render(request,'medchain/transaction_success.html',{"transaction":transaction})
    else:
        form = TransactionForm()
    return render(request, template_name, {"form": form})

def transaction_success(request):
    transaction = request.session.get('transaction')
    return render(request, 'medchain/transaction_success.html',{'transaction':transaction})

def success(request):
    return render(request, 'medchain/success.html')

def route_wallet_info(request):
    return render(request, 'medchain/wallet-info.html',{ 'address': wallet.address, 'balance': wallet.balance })

def route_known_addresses(request):
    known_addresses = set()

    for block in blockchain.chain:
        for transaction in block.data:
            known_addresses.update(transaction['output'].keys())

    return render(request, 'medchain/known-wallet.html',{known_addresses:list(known_addresses)})

def route_unmined_transactions(request):
    
    print(transaction_pool.transaction_data())
    return render(request, 'medchain/pool.html',{"transaction_pool":transaction_pool.transaction_data()})





