"""

    Test KeyPair class

"""
import os
import pytest
import secrets

from convex_api.key_pair import KeyPair
from tests.types import KeyPairInfo


SIGN_HASH_TEXT = '5bb1ce718241bfec110552b86bb7cccf0d95b8a5f462fbf6dff7c48543622ba5'
SIGN_TEXT = '0x7eceffab47295be3891ea745838a99102bfaf525ec43632366c7ec3f54db4822b5d581573aecde94c420554f963baebbf412e4304ad8636886ddfa7b1049f70e'  # noqa: E501

PUBLIC_KEY = '0x5288fec4153b702430771dfac8aed0b21cafca4344dae0d47b97f0bf532b3306'
PUBLIC_KEY_CHECKSUM = '0x5288Fec4153b702430771DFAC8AeD0B21CAFca4344daE0d47B97F0bf532b3306'

def test_key_pair_create_new():
    key_pair = KeyPair()
    assert(key_pair)
    assert(key_pair.public_key)


def test_key_pair_create_from_bytes(test_key_pair_info: KeyPairInfo):
    key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    assert(key_pair)
    assert(key_pair.public_key == test_key_pair_info['public_key'].lower())

def test_key_pair_address_bytes(test_key_pair_info: KeyPairInfo):
    key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    assert(key_pair)
    assert(key_pair.public_key_bytes == KeyPair.hex_to_bytes(test_key_pair_info['public_key']))

def test_key_pair_address_api(test_key_pair_info: KeyPairInfo):
    key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    assert(key_pair)
    assert(key_pair.public_key_api == KeyPair.remove_0x_prefix(test_key_pair_info['public_key']))

def test_key_pair_address_checksum(test_key_pair_info: KeyPairInfo):
    key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    assert(key_pair)
    assert(key_pair.public_key_checksum == test_key_pair_info['public_key'])

def test_key_pair_sign(test_key_pair_info: KeyPairInfo):
    hash_text = SIGN_HASH_TEXT
    key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    sign_data = key_pair.sign(hash_text)
    assert(sign_data == SIGN_TEXT)


def test_key_pair_import_export_to_text(test_key_pair: KeyPair):
    password = 'secret'
    text = test_key_pair.export_to_text(password)
    import_key_pair = KeyPair.import_from_text(text, password)
    assert(import_key_pair)
    assert(import_key_pair.public_key == test_key_pair.public_key)


def test_key_pair_import_export_to_file(test_key_pair: KeyPair):
    filename = '/tmp/private_key.pem'
    password = 'secret'
    if os.path.exists(filename):
        os.remove(filename)

    test_key_pair.export_to_file(filename, password)
    assert(os.path.exists(filename))
    import_key_pair = KeyPair.import_from_file(filename, password)
    assert(import_key_pair)
    assert(import_key_pair.public_key == test_key_pair.public_key)
    os.remove(filename)

def test_key_pair_export_to_mnemonic(test_key_pair: KeyPair):
    words = test_key_pair.export_to_mnemonic
    assert(words)
    new_key_pair = KeyPair.import_from_mnemonic(words)
    assert(new_key_pair)
    assert(test_key_pair.public_key == new_key_pair.public_key)
    assert(test_key_pair.export_to_mnemonic == new_key_pair.export_to_mnemonic)

def test_key_pair_is_equal(test_key_pair: KeyPair):
    key_pair = KeyPair()
    assert(test_key_pair.is_equal(test_key_pair))
    assert(test_key_pair.is_equal(test_key_pair.public_key_api))
    assert(test_key_pair.is_equal(test_key_pair.public_key))
    assert(not key_pair.is_equal(test_key_pair.public_key_checksum))
    assert(not key_pair.is_equal(test_key_pair))
    with pytest.raises(TypeError):
        assert(not key_pair.is_equal(test_key_pair.public_key_bytes)) # type: ignore

def test_key_pair_is_public_key_hex():
    public_key = secrets.token_hex(32)
    assert(KeyPair.is_public_key_hex(public_key))

def test_key_pair_is_public_key():
    public_key = secrets.token_hex(32)
    assert(KeyPair.is_public_key(public_key))

def test_key_pair_is_public_key_checksum():
    public_key = secrets.token_hex(32)
    public_key_checksum = KeyPair.to_public_key_checksum(public_key)
    assert(KeyPair.is_public_key_checksum(public_key_checksum))

def test_key_pair_to_public_key_checksum():
    # generate a ethereum public_key
    # convex public_key to checksum
    public_key_checksum = KeyPair.to_public_key_checksum(PUBLIC_KEY)
    assert(KeyPair.is_public_key_checksum(public_key_checksum))
    assert(public_key_checksum == PUBLIC_KEY_CHECKSUM)