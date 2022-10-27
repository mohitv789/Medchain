
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from medchain.block import Block

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-f915cfba-1778-4472-9876-6beab7abffcf'
pnconfig.publish_key = 'pub-c-915f36e4-6c64-4b4f-bcf0-f2a29c026c8c'
# pnconfig.uuid = str(uuid.uuid1())

CHANNELS = {
    "TEST" : "TEST_CHANNEL",
    "BLOCK" : "BLOCK_CHANNEL"
}

class Listener(SubscribeCallback):

    def __init__(self,blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')
        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                print(f'\n -- Successfully replaced the local chain')
            except Exception as e:
                print(f'\n -- Did not replace chain: {e}')


class PubSub():

    def __init__(self,blockchain):
        self.pubnub = PubNub(pnconfig)
        try:
            self.pubnub.subscribe().channels(["TEST_CHANNEL","BLOCK_CHANNEL"]).execute()
        except Exception as e:
            print(f'Error: {e}')
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self,channel,message):
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self,block):
        self.publish(CHANNELS['BLOCK'],block.to_json())







