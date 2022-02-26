import unittest
import time
from colorama import Fore

from wallet import wallet_adrs

class test_bc(unittest.TestCase):
    
    # use setUp(self) instead of __init__(self)
    def setUp(self):
        self.wallet = wallet_adrs.wallet()

if __name__ == "__main__":
    unittest.main()