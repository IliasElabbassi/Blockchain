from re import S
from colorama import Fore
import unittest
import time

from BC import blockchain
from BC import block

class test_bc(unittest.TestCase):
    # use setUp(self) instead of __init__(self)
    def setUp(self):
        self.bc = blockchain.Blockchain()
        
        self.rv_gg = ["Seulgi", "Irene", "Wendy", "Joy", "Yeri", "Isa", "IU", "Arin", "Hyewon", "Minju"]
        for x in range(0,10):
            blockCreated = block.Block(len(self.bc.chain), self.rv_gg[x], self.bc.chain[-1].hash, time.time())
            blockHash = self.bc.proofOfWork(blockCreated)
            self.bc.add_block(blockCreated, blockHash)

    def test_len(self):
        print(Fore.CYAN+"bc.length() == 11 ?"+Fore.WHITE)
        self.assertEqual(self.bc.length(), 11, 'wrong blockchain length') # 10 for rv_gg + genesis block

    def test_genesis_block(self):
        print(Fore.CYAN+"testing genesis block"+Fore.WHITE)
        data = self.bc.chain[0].data
        self.assertEqual(data, "I am the Genesis Block :)", "wrong genesis block")

    def test_blocks_info(self):
        print(Fore.CYAN+"testing block info"+Fore.WHITE)
        blocks = self.bc.chain[1:-1]
        for block in blocks:
            self.assertIn(block.data, self.rv_gg)

    def test_block_hash(self):
        pass

if __name__ == "__main__":
    unittest.main()