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
        self.nonce = 0
    
    '''
    Method to compute the block
    We concatenate the block information and hash it
    '''
    def computeHash(self, merkle=False):
        if not merkle:
            toHash = json.dumps(self.__dict__, sort_keys=True)
            return hashlib.sha256(toHash.encode()).hexdigest()
        else:
            return self.merkleTree()
            pass
        
    '''
    merkle tree method init
    '''
    def merkleTree(self):
        data = self.__dict__
        merkleBlocks = []
        
        for ele in data:
            merkleBlocks.append(json.dumps(str(ele)+"="+str(data[ele])))
        
        if len(merkleBlocks) % 2 != 0:
            merkleBlocks.append(json.dumps("Fill block"))
           
        for i in range(0, len(merkleBlocks)):
            merkleBlocks[i] = hashlib.sha256(merkleBlocks[i].encode()).hexdigest()
            
        return self.merkleTreeRecursion(merkleBlocks)

    '''
    Recursion method used in merkleTree method
    '''
    def merkleTreeRecursion(self, blocks):
            temp = []
            if len(blocks) != 1:
                if len(blocks) % 2 != 1:
                    for i in range(0, len(blocks), 2):
                        temp.append(hashlib.sha256(json.dumps(blocks[i]+blocks[i+1]).encode()).hexdigest())
                    return self.merkleTreeRecursion(temp)
                else:
                    blocks.append("filling block")
                    for i in range(0, len(blocks), 2):
                        temp.append(hashlib.sha256(json.dumps(blocks[i]+blocks[i+1]).encode()).hexdigest())
                    return self.merkleTreeRecursion(temp)

            return hashlib.sha256(blocks[len(blocks)-1].encode()).hexdigest()
        
if __name__ == "__main__":
    print("Red velvet\n")
    b = Block(1,":)","abcdeer", 1234)
    
    a = b.merkleTree()