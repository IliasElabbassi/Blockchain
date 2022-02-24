import unittest
import time
from colorama import Fore

from BC import blockchain
from BC import block

class test_bc(unittest.TestCase):
    
    # use setUp(self) instead of __init__(self)
    def setUp(self):
        self.bc = blockchain.Blockchain()
        
        rv_gg = ["Seulgi", "Irene", "Wendy", "Joy", "Yeri", "Isa", "IU", "Arin", "Hyewon", "Minju"]
        for x in range(0,10):
            blockCreated = block.Block(len(self.bc.chain), rv_gg[x], self.bc.chain[-1].hash, time.time())
            blockHash = self.bc.proofOfWork(blockCreated)
            self.bc.add_block(blockCreated, blockHash)

    def test_len(self):
        print(Fore.CYAN+"bc.length() == 11 ?"+Fore.WHITE)
        self.assertEqual(self.bc.length(), 11) # 10 for rv_gg + genesis block

if __name__ == "__main__":
    unittest.main()