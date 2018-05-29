from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Wallet:

    def generate_market_root_keypairs(self, marketName):
        """
        Generate root signing keys for a market place
        """
        (self.Sm, self.Pm) = self.generate_RSA()
        print('Generated root key pairs for marketplace: %s' % (marketName))

    def generate_signing_vendor_keypairs(self, marketName, vendorName):
        """
        """
        (self.Svm, self.Pvm) = self.generate_RSA()
        print('Start signing key for vendor %s by marketPlace %s root key.' % (vendorName, marketName))
        self.market_signed_Pvm = self.market_place_sign_vendor()
        self.cross_signed_Pvm = self.vendor_cross_sign(self.market_signed_Pvm)
        print('Generated sigining key pair for marketplace: %s' % (marketName))
    
    def verify(self):
        """
        Verify cross sign vendor's public key
        """
        market_public_key = self.load_market_place_rsa_key().public_key()
        vendor_public_key = self.load_vendor_rsa_key().public_key()

        # Verify market place has signed the vendor public key
        market_public_key.verify(
            self.market_signed_Pvm,
            self.Pvm,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256())

        # Verify vendor has cross sign
        vendor_public_key.verify(
            self.cross_signed_Pvm,
            self.market_signed_Pvm,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256())

    def generate_RSA(self, key_size=2048):
        """
        Generate an RSA keypair with an exponent of 65537 in PEM format
        param: bits The key length in bits
        Return private key and public key
        https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
        """
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=key_size
        )
        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption())
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return (private_key, public_key)

    def load_market_place_rsa_key(self):
        """
        Load market place private key object
        """
        return self._load_rsa_privkey_obj(self.Sm)

    def load_vendor_rsa_key(self):
        """
        Load market place private key object
        """
        return self._load_rsa_privkey_obj(self.Svm)

    def market_place_sign_vendor(self):
        """
        Market Place sign vendor public key
        """
        rsa_key = self.load_market_place_rsa_key()
        return self._sign(rsa_key, self.Pvm)
    
    def vendor_cross_sign(self, data):
        """
        Market Place sign vendor public key
        """
        rsa_key = self.load_vendor_rsa_key()
        return self._sign(rsa_key, data)

    def _load_rsa_privkey_obj(self, private_key):
        """
        Load rsa private key instance by rsa private key
        """
        return crypto_serialization.load_pem_private_key(private_key, None, crypto_default_backend())

    def _sign(self, rsa_key, message):
        """
        Sign a message by private key
        """
        signature = rsa_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
