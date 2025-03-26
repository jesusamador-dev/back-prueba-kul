from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from dataclasses import dataclass


@dataclass
class RSAKeyPair:
    public_key: str
    private_key: str


class RSAKeyGeneratorService:
    def generate_key_pair(self) -> RSAKeyPair:
        private_key_obj = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        private_key_pem = private_key_obj.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode("utf-8")

        public_key_pem = private_key_obj.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")

        return RSAKeyPair(
            public_key=self._clean_key(public_key_pem),
            private_key=self._clean_key(private_key_pem)
        )

    def _clean_key(self, pem_key: str) -> str:
        """
        Elimina las líneas de encabezado, pie y saltos de línea de una clave PEM.
        """
        lines = pem_key.strip().splitlines()
        # Ignorar encabezado y pie ("-----BEGIN ...-----" y "-----END ...-----")
        key_lines = [line for line in lines if not line.startswith("-----")]
        return ''.join(key_lines)
