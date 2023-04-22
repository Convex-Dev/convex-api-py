
from typing import TypedDict


class KeyPairInfo(TypedDict):
    private_hex: int
    private_bytes: bytes
    private_text: str
    private_password: str
    private_mnemonic: str
    public_key: str