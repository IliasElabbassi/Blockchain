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
    
    '''
    add a node into the node list only if there is no node with the exams same property
    '''
    def add_node(self, adresse, url):
        if adresse not in self.nodes:
            node = {
                'adresse' : adresse,
                'url' : url
            }
            self.nodes.append(node)
            return adresse
        else:
            return False
    
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
    append a new transaction to the transaction list
    '''
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
            node_chain = requests.get("{0}/chain".format(node.url))
            temp = len(node_chain)
            if temp > chain_len:
                new_chain = node_chain
                chain_len = temp
        
        self.chain = new_chain
        
        # TODO: notify all the nodes with the new chain

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
            print("signature : "+str(block.signature))
            print("-------------------------------------------------------------\n")

if __name__ == "__main__":
    ###
    start = time.time()
    ###
    
    print("\nAsseul")
    bc = Blockchain()

    public_k = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAj+3tK3MpgjLvQ6xh4np9\ntD1VgR6FJul1AxbRSMYi+fuWTQHggsN6nyvS1x1mb7F8vL0PsZ38ho3iPl8reRGj\nSztN/DUC6ZJlor4SPdapuJ5KXrupgMn9AqysjVhLqU/iAxyr8PEHSVLOFIyn4V92\nCyQ5zz5mV/qKVfMzC1WVcxt1OzI1p4jjNHtnMzlUdSObiX8z4C1AJr0l/tpms5LX\nb8qUAjohJ2d8g/8s12XU7SIdw4dF8Uf9U+XcsFzHv0d0nnfqcFOgne7pczW1cxkw\nFMCWir0cI+iMCOSLB1UG8jKpax/6HBkHKsHH7JQRZu42iDO5zoLCutmQicyxod5/\n0QIDAQAB\n-----END PUBLIC KEY-----'
    false_pubk = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwlrPu3WhUZEVj67MHWzo\nolGwFlyGo2N0meCEgMUbQ/cdw8mtOgnDNIX986gPUllOLyctasubmFozYKHUDmdq\nI3A3aBU1ihMqb5oJkOHKuac1njAXlr+Xvn0KCAI2sXq5Ca3DEKcAVxo3TGzySg6T\nzk8hyvSvGVzoCvp859+CxHq27Xwjula2ZJXtDvrjujqxqItWhSx2gvuFy0K8S0Qd\n+6fVj0f8+O0c3b5A3aBdxw3x8NTUY+OEkayMUkuNPfBwBhrTaTjUvEJH0AFfKUpl\ndryKWbS6FKDjLxURg0JcNONzXcb0RcojTfJz50fCVw5e2iBj5WSS08ovCoJTZkgR\nzwIDAQAB\n-----END PUBLIC KEY-----'
    private_k = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAj+3tK3MpgjLvQ6xh4np9tD1VgR6FJul1AxbRSMYi+fuWTQHg\ngsN6nyvS1x1mb7F8vL0PsZ38ho3iPl8reRGjSztN/DUC6ZJlor4SPdapuJ5KXrup\ngMn9AqysjVhLqU/iAxyr8PEHSVLOFIyn4V92CyQ5zz5mV/qKVfMzC1WVcxt1OzI1\np4jjNHtnMzlUdSObiX8z4C1AJr0l/tpms5LXb8qUAjohJ2d8g/8s12XU7SIdw4dF\n8Uf9U+XcsFzHv0d0nnfqcFOgne7pczW1cxkwFMCWir0cI+iMCOSLB1UG8jKpax/6\nHBkHKsHH7JQRZu42iDO5zoLCutmQicyxod5/0QIDAQABAoIBAAf4R9LJHLpN8bvQ\nltcAq2dIoix1MTBXaxhRsiMSfatUCB2ZhgIXqvmXZqRsx1hV/q9A1NakBfC5eJa1\nlGWu2Vj4HrhhgxjF94TMe5wa/+juMvYN9DPie3UjdKabBg2JE93SP58m6Z1gzXKL\n21v6ekHhrqXQMcCbaf+aaPAuvAjUnh/IF1JYvYBb7lxs/LFpJeUaxfMh25/jQ+y3\nxXKs6taDG9ljNEVn3G0vft5B+jJ/uEjqaSclWmfPUuD31D1vEsKQ5ikqczXULblM\nfp25cquKOHoCCPFJjAFPSTej/a+khZ6VeY3e67zxzkRbeH6SH0jXxuhe1q2eVW4Q\nOmADWkECgYEAtvNSvPxutp+Y1ALH57U7++pOUW3TniSg82FitMD6cfnGKNSTuXAw\nimP0277CU3om0aTmQ+sY3LDXyMItfn938dfvLRxzYyZX/fpWIW0nvAhtRYXJUjjE\nvgY0JW5Te62rhogmFoJmD9qQXZncgEkKaP6ZYKozAqD0r0oRi11jOHkCgYEAyWX6\nw5/hrhdb25yPickEGezhzVxsxGFr2pQtZtvIwKSCPdrUNibN2UpxKhp71Bd+T4gK\nmxAYTaG72Mt/jJlgvrEc+CfieI/4TO2/WJxWBQO6GKO1SpDhi1uNcOPESi63KE+a\n/8sLqoBn7hXteNja/sdk5PKGsyjZKpXjU/ZW3BkCgYAT0fCYwNBNwKSR82ss0xmY\nhR3O/JL8gwNc2qQS6QU469JoAf+vC1R26bVRSS1MVeN2uuKnYQTkg9Qcz8yV88FO\n1hH3VSm7CCBoR4KlRGoVmOQdsAzLd5L48zsbAwTQVVRL0twtfBsKhKc3PMACtecG\n0O5U5pt4IW/gvamA67EgIQKBgQCC9s7XkUtXQxdXuvpYNiB1n2XCfjy4g0V4cO0J\nOxjTtOaAxKFEyX0ItPDb2Tb214QqwaNr7E5xhR+7PbGmw0J3HoNhF8accbqcg+nu\n/FKvlhnY1fQZFhek4JccdvB48OHn08ROXEIs0K1E1HuFHzdhgFYqz08qiACYQbn/\nKmyXWQKBgG2W5H4FwEUMJ2y0g5zkLhwVyM+ly9UCfyfpPssfiTAOH/w7E1/togH4\n521KSKckCynTLYkwK0wCGk1CdlLGyWr4DuHv8K7B5IreUkHkxGS2i6KcQR7aG5Vj\nWMZlLai4JDob04kyAYjA1yjmrBMLORslQDSSR9zek127JILxCrjc\n-----END RSA PRIVATE KEY-----'
    address = b'RVx3k8tLpY4vsSYYvLVXjKp7D8hXLJqgCkxSEgHj67jGdb1giDWfiPzwWd'

    for i in bc.chain:
        print("previous : "+i.previousHash + "  new : "+ i.hash)
        pass
    
    rv_gg = ["Seulgi", "Irene", "Wendy", "Joy", "Yeri", "Isa", "IU", "Arin", "Hyewon", "Minju"]
    for gg in rv_gg:
        print('\n\n===== new block =====')
        #blockCreated = block.Block(len(bc.chain), str(uuid4()), bc.chain[-1].hash, time.time())
        blockCreated = block.Block(len(bc.chain), gg, bc.chain[-1].hash, time.time())
        print(blockCreated.__dict__)
        blockCreated.sign(private_k)
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
        print("\n")
    else:
        print("Chain corupted")

    for b in bc.chain[1:-1]:
        try:
            b.verify(public_k)
            print(str(b.index)+" : Verified OK")
            print()
        except:
            print(str(b.index)+" : error in the verification of the signature")
            print()

    ###
    print((time.time() - start))
    ###
    
        
    