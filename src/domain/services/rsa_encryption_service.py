from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import base64


class RSAEncryptionService:
    def __init__(self, private_key_pem: str = None, public_key_pem: str = None):
        self.private_key = (
            serialization.load_pem_private_key(
                self._reconstruct_private_pem(private_key_pem).encode(), password=None
            )
            if private_key_pem else None
        )

        self.public_key = (
            serialization.load_pem_public_key(
                self._reconstruct_public_pem(public_key_pem).encode()
            )
            if public_key_pem else None
        )

    def _reconstruct_private_pem(self, clean_key: str) -> str:
        return (
            "-----BEGIN PRIVATE KEY-----\n"
            + "\n".join(clean_key[i:i + 64] for i in range(0, len(clean_key), 64))
            + "\n-----END PRIVATE KEY-----\n"
        )

    def _reconstruct_public_pem(self, clean_key: str) -> str:
        return (
            "-----BEGIN PUBLIC KEY-----\n"
            + "\n".join(clean_key[i:i + 64] for i in range(0, len(clean_key), 64))
            + "\n-----END PUBLIC KEY-----\n"
        )

    def encrypt(self, plain_text: str) -> str:
        if not self.public_key:
            raise ValueError("Private key is required for encryption.")
        encrypted = self.public_key.encrypt(
            plain_text.encode(),
            padding.PKCS1v15()
        )
        return base64.b64encode(encrypted).decode()

    def decrypt(self, encrypted_text: str) -> str:
        if not self.private_key:
            raise ValueError("Public key is required for decryption.")
        encrypted_bytes = base64.b64decode(encrypted_text)
        decrypted = self.private_key.decrypt(
            encrypted_bytes,
            padding.PKCS1v15()
        )
        return decrypted.decode()
