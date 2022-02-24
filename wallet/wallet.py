from Crypto.PublicKey import RSA
from BC.utils import calculate_hash

class wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.initialize_keys()

    def initialize_keys(self):
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey().exportKey()
    
    def get_privateKey(self):
        return self.private_key.exportKey()

    def get_publicKey(self):
        return self.private_key.exportKey()


if __name__ == "__main__":
    wallet = wallet()
    print("private key: {0}".format(wallet.get_privateKey()))
    print("public key: {0}".format(wallet.get_publicKey()))