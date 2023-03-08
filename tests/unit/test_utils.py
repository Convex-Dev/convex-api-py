"""


    Test  Utils

"""
import secrets

PUBLIC_KEY = '0x5288fec4153b702430771dfac8aed0b21cafca4344dae0d47b97f0bf532b3306'
PUBLIC_KEY_CHECKSUM = '0x5288Fec4153b702430771DFAC8AeD0B21CAFca4344daE0d47B97F0bf532b3306'

from convex_api.utils import (
    is_public_key,
    is_public_key_hex,
    is_public_key_checksum,
    to_public_key_checksum
)

def test_utils_is_public_key_hex():
    public_key = secrets.token_hex(32)
    assert(is_public_key_hex(public_key))

def test_utils_is_public_key():
    public_key = secrets.token_hex(32)
    assert(is_public_key(public_key))

def test_utils_is_public_key_checksum():
    public_key = secrets.token_hex(32)
    public_key_checksum = to_public_key_checksum(public_key)
    assert(is_public_key_checksum(public_key_checksum))

def test_utils_to_public_key_checksum():
    # generate a ethereum public_key
    # convex public_key to checksum
    public_key_checksum = to_public_key_checksum(PUBLIC_KEY)
    assert(is_public_key_checksum(public_key_checksum))
    assert(public_key_checksum == PUBLIC_KEY_CHECKSUM)