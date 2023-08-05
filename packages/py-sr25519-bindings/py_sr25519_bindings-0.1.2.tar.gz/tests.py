import unittest

import bip39
import sr25519


class MyTestCase(unittest.TestCase):
    message = b"test"
    seed = bip39.bip39_to_mini_secret('daughter song common combine misery cotton audit morning stuff weasel flee field','')
    chain_code = bytes.fromhex('7eadeb0f985ffcab9e50f25a19c1e4c8c2f4cd742049fc35e07c684040057e9a')
    child_index = b"\x01\x02\x03\x04"

    def test_sign_and_verify_message(self):
        # Get private and public key from seed
        public_key, private_key = sr25519.pair_from_seed(bytes(self.seed))

        # Generate signature
        signature = sr25519.sign(
            (public_key, private_key),
            self.message
        )

        # Verify message with signature
        self.assertTrue(sr25519.verify(signature, self.message, public_key))

    def test_derive_soft(self):
        # Get private and public key from seed
        public_key, private_key = sr25519.pair_from_seed(bytes(self.seed))

        # Private derivation
        child_chain_priv, child_pubkey_priv, child_privkey = sr25519.derive_keypair(
            (self.chain_code, public_key, private_key),
            self.child_index
        )

        # Public derivation
        child_chain_pub, child_pubkey_pub = sr25519.derive_pubkey(
            (self.chain_code, public_key),
            self.child_index
        )

        # Assert that the chain code and public key are the same regardless of
        # derivation method
        self.assertEqual(child_chain_priv, child_chain_pub)
        self.assertEqual(child_pubkey_priv, child_pubkey_pub)

        # Test that signatures with the derived private key are valid
        signature = sr25519.sign(
            (child_pubkey_priv, child_privkey),
            self.message
        )

        self.assertTrue(sr25519.verify(signature, self.message, child_pubkey_pub))

    def test_derive_hard(self):
        # Get private and public key from seed
        public_key, private_key = sr25519.pair_from_seed(bytes(self.seed))

        # Private derivation
        _, child_pubkey, child_privkey = sr25519.hard_derive_keypair(
            (self.chain_code, public_key, private_key),
            self.child_index
        )

        # Test that signatures with the derived private key are valid
        signature = sr25519.sign(
            (child_pubkey, child_privkey),
            self.message
        )

        self.assertTrue(sr25519.verify(signature, self.message, child_pubkey))

s
if __name__ == '__main__':
    unittest.main()
