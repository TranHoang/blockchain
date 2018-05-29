import unittest
from wallet import Wallet

class TestSignature(unittest.TestCase):

    def setUp(self):
        self.wallet = Wallet()
    
    def test_converage(self):
        self.test_generate_market_place_key()
        self.test_generate_signing_vendor_keypairs()

    def generate_market_place_key(self):
        """
        Make sure the system can generate private key pairs for a Market Place
        """
        self.wallet.generate_market_root_keypairs('Amazon')
        
        self.assertNotEqual(self.wallet.Sm, None, 'Cant generate private key for market place')
        self.assertNotEqual(self.wallet.Pm, None,'Cant generate public key for market place')

    def generate_signing_vendor_keypairs(self):
        """
        Make sure the system can generate private key pairs
        and cross sign public key for a Market Place
        """
        self.wallet.generate_market_root_keypairs('Amazon')
        self.wallet.generate_signing_vendor_keypairs('Amazon', 'BHPhoto')

        self.assertNotEqual(self.wallet.market_signed_Pvm, None)
        self.assertNotEqual(self.wallet.cross_signed_Pvm, None)


if __name__ == '__main__':
    unittest.main()