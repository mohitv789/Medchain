
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from medchain.block import Block
from medchain.transaction import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-f915cfba-1778-4472-9876-6beab7abffcf'
pnconfig.publish_key = 'pub-c-915f36e4-6c64-4b4f-bcf0-f2a29c026c8c'
# pnconfig.uuid = str(uuid.uuid1())

CHANNELS = {
    "TEST" : "TEST_CHANNEL",
    "BLOCK" : "BLOCK_CHANNEL",    
    "TRANSACTION": "TRANSACTION_CHANNEL"
}

class Listener(SubscribeCallback):

    def __init__(self,blockchain,transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')
        if message_object.channel == "BLOCK_CHANNEL":
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                print(f'\n -- Successfully replaced the local chain')
            except Exception as e:
                print(f'\n -- Did not replace chain: {e}')
        elif message_object.channel == "TRANSACTION_CHANNEL":
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n -- Set the new transaction in the transaction pool')


class PubSub():

    def __init__(self,blockchain,transaction_pool):
        self.pubnub = PubNub(pnconfig)
        try:
            self.pubnub.subscribe().channels(["TEST_CHANNEL","BLOCK_CHANNEL","TRANSACTION_CHANNEL"]).execute()
        except Exception as e:
            print(f'Error: {e}')
        self.pubnub.add_listener(Listener(blockchain,transaction_pool))

    def publish(self,channel,message):
        self.pubnub.unsubscribe().channels([channel]).execute()
        self.pubnub.publish().channel(channel).message(message).sync()
        self.pubnub.subscribe().channels([channel]).execute()

    def broadcast_block(self,block):
        self.publish(CHANNELS['BLOCK'],block.to_json())

    def broadcast_transaction(self, transaction):
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())







