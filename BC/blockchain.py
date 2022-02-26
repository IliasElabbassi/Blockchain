from BC import block
import time
from uuid import uuid4
import requests
import json

'''
Main file to modelise a blockchain
'''
class Blockchain:
    difficulty = 3
    '''
    Blockchain class constructor
    '''
    def __init__(self):
        self.chain = []
        self.unconfirmedBlocks = []
        self.nodes = []

        self.generateGenesisBlock()

    def length(self):
        return len(self.chain)

    @property
    def getChain(self):
        return self.chain
    
    @property
    def getNodes(self):
        return self.nodes
    
    def add_node(self, adresse, url):
        if adresse not in self.nodes:
            node = {
                'adresse' : adresse,
                'url' : url
            }
            #self.nodes.append(json.dumps(node))
            self.nodes.append(node)
    
    '''
    Generate and add the genesis block to the chain
    '''
    def generateGenesisBlock(self):
        genesisBlock = block.Block(0, "I am the Genesis Block :)", "Asseul", time.time())
        genesisBlock.hash = genesisBlock.computeHash(merkle=True)
        self.chain.append(genesisBlock)

    '''
    check if a block can be added to the chain and add it
    '''
    def add_block(self, block, proof):
        previousHash = self.chain[-1].hash
        
        if previousHash != block.previousHash:
            print("previous hash error")
            return False

        if not self.isValid(block, proof):
            print("validity error")
            return False
        
        block.hash = proof
        self.chain.append(block)

        return True

    '''
    Find the nonce on of block
    '''
    def proofOfWork(self, block):
        block.nonce = 0 
        computedHash = block.computeHash(merkle=True)
        
        while not computedHash.startswith('0'*Blockchain.difficulty):
            block.nonce += 1
            computedHash = block.computeHash(merkle=True)

        return computedHash
    
    def new_transaction(self, transaction):
        self.unconfirmedBlocks.append(transaction)
        return True

    '''
    Check if a hash if valid regarding it's block
    A hash if valid if it starts with a certain number of zeros according to the difficulty of the blockchain
    and if we re-compute the hash we obtain the exact same hash
    '''
    def isValid(self, block, blockHash):
        return (blockHash.startswith('0'*Blockchain.difficulty) and blockHash == block.computeHash(merkle=True))
    
    """
    Check if the blockchain is valid or not thanks to the cryptographic function
    we can check the previous hash of the block with the hash of the previous block
    if their are not the same the chain is corrupted
    """
    def checkChain(self):
        for i in range(len(self.chain)-1):
            previous_hash = self.chain[i].hash
            current_hash = self.chain[i+1].previousHash
            
            print("previous : "+previous_hash + "  current : "+ current_hash)
            
            if not previous_hash == current_hash:
                print("\n=================")
                print("previous : "+previous_hash + "  new : "+ current_hash)
                print("=================\n")
                return False
        
        return True
    
    def consensus(self):
        chain_len = len(self.chain)
        new_chain = self.chain
        
        for node in self.nodes:
            node_chain = requests.get("{0}/chain".formar(node))
            temp = len(node_chain)
            if temp > chain_len:
                new_chain = node_chain
                chain_len = temp
        
        self.chain = new_chain
        
        return new_chain
            
    def printChain(self):
        for block in self.chain:
            print("\n-------------------------------------------------------------")
            print("index: "+str(block.index))
            print("timestamp: "+str(block.timestamp))
            print("data: "+str(block.data))
            print("nonce: "+str(block.nonce))
            print("hash: "+str(block.hash))
            print("previous hash: "+str(block.previousHash))
            print("-------------------------------------------------------------\n")

if __name__ == "__main__":
    ###
    start = time.time()
    ###
    
    print("\nAsseul")
    bc = Blockchain()
    public_k =  b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqOLbbAoriuMhpNr8XEBg\nGtbOiUxC6oB4FeLNTSc7od8QIk4IjnqIWf8mz/j5IaromWlwCs2QSNYW6oO2B5cs\nWEy0Xikh/vXeOFEPmtTmDkOkCzqP0jS8/racJDORp5Mb0vR03UlsuGoq2w0OYZeZ\nO6b95ivTdRW900Mnh7MpiKorlGG0yzQNdLkElquOdqiGlekRxFB3PzUkc4NcW4Xc\nrPeNVdsdcxI14clOUnjsEwNeneztO1/iYMLHgEVIL7suvtPXXiT60ydP+8o+CTRk\nnBT/GA9xtGGPigUmtOggx+O5ahe9bkYyBxmo6eMfUjS9Ey13EwBbJfgVSNqEBuK0\nFQIDAQAB\n-----END PUBLIC KEY-----'
    false_pubk = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwlrPu3WhUZEVj67MHWzo\nolGwFlyGo2N0meCEgMUbQ/cdw8mtOgnDNIX986gPUllOLyctasubmFozYKHUDmdq\nI3A3aBU1ihMqb5oJkOHKuac1njAXlr+Xvn0KCAI2sXq5Ca3DEKcAVxo3TGzySg6T\nzk8hyvSvGVzoCvp859+CxHq27Xwjula2ZJXtDvrjujqxqItWhSx2gvuFy0K8S0Qd\n+6fVj0f8+O0c3b5A3aBdxw3x8NTUY+OEkayMUkuNPfBwBhrTaTjUvEJH0AFfKUpl\ndryKWbS6FKDjLxURg0JcNONzXcb0RcojTfJz50fCVw5e2iBj5WSS08ovCoJTZkgR\nzwIDAQAB\n-----END PUBLIC KEY-----'
    private_k = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAqOLbbAoriuMhpNr8XEBgGtbOiUxC6oB4FeLNTSc7od8QIk4I\njnqIWf8mz/j5IaromWlwCs2QSNYW6oO2B5csWEy0Xikh/vXeOFEPmtTmDkOkCzqP\n0jS8/racJDORp5Mb0vR03UlsuGoq2w0OYZeZO6b95ivTdRW900Mnh7MpiKorlGG0\nyzQNdLkElquOdqiGlekRxFB3PzUkc4NcW4XcrPeNVdsdcxI14clOUnjsEwNenezt\nO1/iYMLHgEVIL7suvtPXXiT60ydP+8o+CTRknBT/GA9xtGGPigUmtOggx+O5ahe9\nbkYyBxmo6eMfUjS9Ey13EwBbJfgVSNqEBuK0FQIDAQABAoIBABbR/JM3NpYAReII\nQxRWEIZf4y2TM/GK5W8To+kadYjUYtI32BkkfnsmqoBspIFDnkVohV64Uxg8cYFD\nxdt1tmTCDJcymKjiYSIb9e9WeDWSNz7bLWbagHUsiKGtpC9QBfD13jquerXahqrt\nszVFrktsr58j6eFGzE0ZJGTGNUUFfM8ymNRpyoEF5SIALTTw7l2dkA+p7RsjS1mv\nL6NCLDa/9I8PRueHTPkeijrV+6BuHAwoxltO0bBuMcqIvGdydxpxveCtCejziYU0\nlqxVJ7OGc0fEBpflCKzEj0kw2UEwTsenXYCHmQrkufpcT1vz1D2eNdgliELUszZA\nj9pWzXsCgYEAtrR0xv3H2t40RtOp9lSQvRs3aaxHc/VjtrIVua4iA3gp84P0SjQb\ndgtGWU9NS0KRjzT7KetyUcBRDbasRmACWZi0enXiVKTfYefIHjTgVpqCzpZkfVPa\nEfSdl9UCXnukLKbgbITOMyvDYGlsbTjbF3uUtClxhl3ijq0Pfy/6ohcCgYEA7KM8\nELz4XQCSlX6+fc76C7FrhO87KVSIFoZHvc9DDW6OvqJz9TvOkP5vFjetPay8Up5F\ne1PTWE47SNIRLo5+WV1t2tmTw5/dRceg7+prYgnG1m+BHQ3CorGKTf8ZtZO1XiJV\n6UrNEkiajfd1INcZyD2bD4nnKf5cb/XHDi4IUrMCgYAyjpbt5ZXjG6/NlY6nilkO\n6zQXOsP+831nNbpLSkNBQIQjTXVQ/0BGFvKdjhMuazpKLXf+7pcQxi3npI/hXXno\n/xeZ93rsvz7NIc0/hpQ5gsIFlpoyD/z9EPp25Eumh4IzlO3vOYSxpj+HM0T8qEoA\nIoNQo1M1wk8J+huar1UkewKBgHE3C9bKQl1kl70UfZj9fJ45jUJ1nq2Adven2Q0T\n63WyrnLAkJAExCiUwpszmhwG17cDaCTADz6Rd0W402Wd4Q9qZtOtA0g15QysnPAM\nDMJEATC4+mHnInbqUExOv4MjH0PhU48hLYoQ2HkRqqVCpGAsMVK23LU3sAwU396F\n4Y+HAoGAM0qmnSa3h33kTJaUDFdZf0huTvOaTyImRLSijDajur4TYOHp5ZCEGdDt\nBbsUJJ5rBfM1oDLr6yW8a0yOFt2jGYQd3oifwbkHa2HPM5bJIzZ+obuCx/jJZ3Ap\nOU2mCTxdqUQJzTnpzFSMpCNeU+uKQes9ig2JgtwPAbriLrwf82c=\n-----END RSA PRIVATE KEY-----'
    
    for i in bc.chain:
        print("previous : "+i.previousHash + "  new : "+ i.hash)
        pass
    
    rv_gg = ["Seulgi", "Irene", "Wendy", "Joy", "Yeri", "Isa", "IU", "Arin", "Hyewon", "Minju"]
    for gg in rv_gg:
        print('\n\n===== new block =====')
        #blockCreated = block.Block(len(bc.chain), str(uuid4()), bc.chain[-1].hash, time.time())
        blockCreated = block.Block(len(bc.chain), gg, bc.chain[-1].hash, time.time())
        print(blockCreated.__dict__)
        blockHash = bc.proofOfWork(blockCreated)
        print('proof of work : '+blockHash)
        print("adding block ...")
        done = bc.add_block(blockCreated, blockHash)
        if done:
            for i in bc.chain:
                print("previous : "+i.previousHash + "  new : "+ i.hash)
        else:
            print('Error while adding block')
                
    bc.printChain()

    print("\n\n==== Check Chain validity ====")
    valid = bc.checkChain()
    if valid:
        print("Chain valid !")
        pass
    else:
        print("Chain corupted")
        pass

    ###
    print((time.time() - start))
    ###
    
        
    