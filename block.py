import hashlib
import json

'''
Class that modelise a block
'''
class Block:
    '''
    Block class constructor
    index: the index of the block (i.e the index of the previous block + 1)
    data: the data to store
    previousHash: the hash of the previous block (i.e index-1)
    timestamp: date of creation concerning this block
    hash: this block hash
    nonce: the nonce to add to the hash to validate the block
    '''
    def __init__(self, index, data, previousHash, timestamp):
        self.data = data
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.hash = ""
        self.nonce = 0
    
    '''
    Method to compute the block
    We concatenate the block information and hash it
    '''
    def computeHash(self):
        toHash = json.dumps(self.__dict__, sort_keys=True)

        return hashlib.sha256(toHash.encode()).hexdigest()

if __name__ == "__main__":
    print("Red velvet")
    b = Block(1,"red velvet","abcdeer", 1234)
    print(b.__dict__)