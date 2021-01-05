import block
import time
from uuid import uuid4

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

        self.generateGenesisBlock()

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
        
if __name__ == "__main__":
    print("\nAsseul")
    bc = Blockchain()
    for i in bc.chain:
        print("previous : "+i.previousHash + "  new : "+ i.hash)
    
        
    for x in range(0,10):
        print('\n\n===== new block =====')
        blockCreated = block.Block(len(bc.chain), str(uuid4()), bc.chain[-1].hash, time.time())
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
        
    
    print("\n\n==== Check Chain validity ====")
    valid = bc.checkChain()
    if valid:
        print("Chain valid !")
    else:
        print("Chain corupted")