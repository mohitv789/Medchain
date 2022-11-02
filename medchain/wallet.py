import uuid, json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from medchain.config import STARTING_BALANCE
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature


class Wallet:

    def __init__(self, blockchain=None):
        self.blockchain = blockchain
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(ec.SECP256K1(),default_backend())
        self.public_key = self.private_key.public_key()        
        self.serialize_public_key()
        
    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)

    def sign(self,data):
        return decode_dss_signature(self.private_key.sign(json.dumps(data).encode('utf-8'),ec.ECDSA(hashes.SHA256())))
    
    def serialize_public_key(self):
        self.public_key = self.public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
        
   
    @staticmethod
    def verify(public_key,data,signature):
        deserialized_public_Key = serialization.load_pem_public_key(public_key.encode('utf-8'),default_backend())
        (r,s) = signature
        try:
            deserialized_public_Key.verify(encode_dss_signature(r,s),json.dumps(data).encode('utf-8'),ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False

    @staticmethod
    def calculate_balance(blockchain, address):
        balance = STARTING_BALANCE

        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if transaction['input']['address'] == address:
                    balance = transaction['output'][address]
                elif address in transaction['output']:
                    balance += transaction['output'][address]

        return balance



