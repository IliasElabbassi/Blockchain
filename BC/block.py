from tkinter.messagebox import NO
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import json

from BC import utils

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
    signature : block data hashed and signed by a private key
    '''
    def __init__(self, index, data, previousHash, timestamp):
        utils.init_logging("block.log")
        
        self.data = data
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.nonce = 0

        self.signature = None
    
    '''
    Method to compute the block
    We concatenate the block information and hash it
    '''
    def computeHash(self, merkle=False):
        if not merkle:
            toHash = json.dumps(self.__dict__, sort_keys=True)
            hash = SHA256.new()
            hash.update(toHash.encode())
            return hash.hexdigest()
        else:
            return self.merkleTree()

    '''
    convert the data to byte
    '''
    def blockToBytes(self):
        b_data = self.toJson()
        return json.dumps(b_data, indent=2).encode("utf-8")
    
    '''
    Sign the data by using a private key
    '''
    def sign(self, owner_pk: bytes):
        print("in sign --------------")
        datas = self.blockToBytes()
        hash_obj = SHA256.new(datas)
        key = RSA.import_key(owner_pk)
        self.signature = pkcs1_15.new(key).sign(hash_obj)
        return self.signature
    
    '''
    Verify the signature by using the public key corresponding to the private key that signed the data
    '''
    def verify(self, pubk):
        datas = self.blockToBytes()
        hash_obj = SHA256.new(datas)
        key = RSA.import_key(pubk)
        try:
            pkcs1_15.new(key).verify(hash_obj, self.signature)
            print("The signature is valid.")
        except (ValueError, TypeError):
            print("The signature is not valid.")
            raise

    '''
    merkle tree method init
    '''
    def merkleTree(self):
        #data = self.__dict__
        data = {
            'index' : self.index,
            'data' : self.data,
            'previousHash' : self.previousHash,
            'timestamp' : self.timestamp,
            'nonce': self.nonce
        }

        merkleBlocks = []
        
        for ele in data:
            merkleBlocks.append(json.dumps(str(ele)+"="+str(data[ele])))
        
        if len(merkleBlocks) % 2 != 0:
            merkleBlocks.append(json.dumps("Fill block"))
           
        for i in range(0, len(merkleBlocks)):
            hash = SHA256.new()
            hash.update(merkleBlocks[i].encode())
            merkleBlocks[i] = hash.hexdigest()
            
        return self.merkleTreeRecursion(merkleBlocks)

    '''
    Recursion method used in merkleTree method
    '''
    def merkleTreeRecursion(self, blocks):
            temp = []
            if len(blocks) != 1:
                if len(blocks) % 2 != 1:
                    for i in range(0, len(blocks), 2):
                        hash = SHA256.new()
                        hash.update(json.dumps(blocks[i]+blocks[i+1]).encode())
                        temp.append(hash.hexdigest())
                    return self.merkleTreeRecursion(temp)
                else:
                    blocks.append("filling block")
                    for i in range(0, len(blocks), 2):
                        hash = SHA256.new()
                        hash.update(json.dumps(blocks[i]+blocks[i+1]).encode())
                        temp.append(hash.hexdigest())
                    return self.merkleTreeRecursion(temp)

            hash = SHA256.new() 
            hash.update(blocks[len(blocks)-1].encode())
            return hash.hexdigest()
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.toJson2(), sort_keys=True)
    
    def toJson(self):
        return {
            'index' : self.index,
            'data' : self.data,
            'previousHash' : self.previousHash,
            'timestamp' : self.timestamp,
        }
        
if __name__ == "__main__":
    print("Red velvet\n")
    b = Block(1,":)","abcdeer", 1234)
    
    a = b.computeHash(merkle=True)
    c = b.computeHash()
    abis = b.computeHash(merkle=True)
    cbis = b.computeHash()

    public_k =  b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqOLbbAoriuMhpNr8XEBg\nGtbOiUxC6oB4FeLNTSc7od8QIk4IjnqIWf8mz/j5IaromWlwCs2QSNYW6oO2B5cs\nWEy0Xikh/vXeOFEPmtTmDkOkCzqP0jS8/racJDORp5Mb0vR03UlsuGoq2w0OYZeZ\nO6b95ivTdRW900Mnh7MpiKorlGG0yzQNdLkElquOdqiGlekRxFB3PzUkc4NcW4Xc\nrPeNVdsdcxI14clOUnjsEwNeneztO1/iYMLHgEVIL7suvtPXXiT60ydP+8o+CTRk\nnBT/GA9xtGGPigUmtOggx+O5ahe9bkYyBxmo6eMfUjS9Ey13EwBbJfgVSNqEBuK0\nFQIDAQAB\n-----END PUBLIC KEY-----'
    false_pubk = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwlrPu3WhUZEVj67MHWzo\nolGwFlyGo2N0meCEgMUbQ/cdw8mtOgnDNIX986gPUllOLyctasubmFozYKHUDmdq\nI3A3aBU1ihMqb5oJkOHKuac1njAXlr+Xvn0KCAI2sXq5Ca3DEKcAVxo3TGzySg6T\nzk8hyvSvGVzoCvp859+CxHq27Xwjula2ZJXtDvrjujqxqItWhSx2gvuFy0K8S0Qd\n+6fVj0f8+O0c3b5A3aBdxw3x8NTUY+OEkayMUkuNPfBwBhrTaTjUvEJH0AFfKUpl\ndryKWbS6FKDjLxURg0JcNONzXcb0RcojTfJz50fCVw5e2iBj5WSS08ovCoJTZkgR\nzwIDAQAB\n-----END PUBLIC KEY-----'
    private_k = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAqOLbbAoriuMhpNr8XEBgGtbOiUxC6oB4FeLNTSc7od8QIk4I\njnqIWf8mz/j5IaromWlwCs2QSNYW6oO2B5csWEy0Xikh/vXeOFEPmtTmDkOkCzqP\n0jS8/racJDORp5Mb0vR03UlsuGoq2w0OYZeZO6b95ivTdRW900Mnh7MpiKorlGG0\nyzQNdLkElquOdqiGlekRxFB3PzUkc4NcW4XcrPeNVdsdcxI14clOUnjsEwNenezt\nO1/iYMLHgEVIL7suvtPXXiT60ydP+8o+CTRknBT/GA9xtGGPigUmtOggx+O5ahe9\nbkYyBxmo6eMfUjS9Ey13EwBbJfgVSNqEBuK0FQIDAQABAoIBABbR/JM3NpYAReII\nQxRWEIZf4y2TM/GK5W8To+kadYjUYtI32BkkfnsmqoBspIFDnkVohV64Uxg8cYFD\nxdt1tmTCDJcymKjiYSIb9e9WeDWSNz7bLWbagHUsiKGtpC9QBfD13jquerXahqrt\nszVFrktsr58j6eFGzE0ZJGTGNUUFfM8ymNRpyoEF5SIALTTw7l2dkA+p7RsjS1mv\nL6NCLDa/9I8PRueHTPkeijrV+6BuHAwoxltO0bBuMcqIvGdydxpxveCtCejziYU0\nlqxVJ7OGc0fEBpflCKzEj0kw2UEwTsenXYCHmQrkufpcT1vz1D2eNdgliELUszZA\nj9pWzXsCgYEAtrR0xv3H2t40RtOp9lSQvRs3aaxHc/VjtrIVua4iA3gp84P0SjQb\ndgtGWU9NS0KRjzT7KetyUcBRDbasRmACWZi0enXiVKTfYefIHjTgVpqCzpZkfVPa\nEfSdl9UCXnukLKbgbITOMyvDYGlsbTjbF3uUtClxhl3ijq0Pfy/6ohcCgYEA7KM8\nELz4XQCSlX6+fc76C7FrhO87KVSIFoZHvc9DDW6OvqJz9TvOkP5vFjetPay8Up5F\ne1PTWE47SNIRLo5+WV1t2tmTw5/dRceg7+prYgnG1m+BHQ3CorGKTf8ZtZO1XiJV\n6UrNEkiajfd1INcZyD2bD4nnKf5cb/XHDi4IUrMCgYAyjpbt5ZXjG6/NlY6nilkO\n6zQXOsP+831nNbpLSkNBQIQjTXVQ/0BGFvKdjhMuazpKLXf+7pcQxi3npI/hXXno\n/xeZ93rsvz7NIc0/hpQ5gsIFlpoyD/z9EPp25Eumh4IzlO3vOYSxpj+HM0T8qEoA\nIoNQo1M1wk8J+huar1UkewKBgHE3C9bKQl1kl70UfZj9fJ45jUJ1nq2Adven2Q0T\n63WyrnLAkJAExCiUwpszmhwG17cDaCTADz6Rd0W402Wd4Q9qZtOtA0g15QysnPAM\nDMJEATC4+mHnInbqUExOv4MjH0PhU48hLYoQ2HkRqqVCpGAsMVK23LU3sAwU396F\n4Y+HAoGAM0qmnSa3h33kTJaUDFdZf0huTvOaTyImRLSijDajur4TYOHp5ZCEGdDt\nBbsUJJ5rBfM1oDLr6yW8a0yOFt2jGYQd3oifwbkHa2HPM5bJIzZ+obuCx/jJZ3Ap\nOU2mCTxdqUQJzTnpzFSMpCNeU+uKQes9ig2JgtwPAbriLrwf82c=\n-----END RSA PRIVATE KEY-----'
    sign_prv = b.sign(private_k)

    # print(a)
    # print(abis)

    # print(c)
    # print(cbis)

    print('\n')
    print(sign_prv)
    b.verify(public_k)
    b.verify(false_pubk)