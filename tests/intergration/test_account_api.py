"""
    Test account based functions

"""

import pytest
import secrets

from convex_api import (
    API,
    KeyPair,
)
from tests.types import KeyPairInfo

TEST_ACCOUNT_NAME = 'test.convex-api'

@pytest.fixture
def account_name():
    return f'{TEST_ACCOUNT_NAME}-{secrets.token_hex(8)}'

def test_account_api_create_account(convex_url: str):

    convex = API(convex_url)
    key_pair = KeyPair()
    result = convex.create_account(key_pair)
    assert(result)


def test_account_api_multi_create_account(convex_url: str):
    convex = API(convex_url)
    key_pair = KeyPair()
    account_1 = convex.create_account(key_pair)
    assert(account_1)
    account_2 = convex.create_account(key_pair)
    assert(account_2)

    assert(account_1.public_key == account_1.public_key)
    assert(account_1.public_key == account_2.public_key)
    assert(account_1.address != account_2.address)


def test_account_name(convex_url: str, test_key_pair_info: KeyPairInfo, account_name: str):
    convex = API(convex_url)
    import_key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    if convex.resolve_account_name(account_name):
        account = convex.load_account(account_name, import_key_pair)
    else:
        account = convex.create_account(import_key_pair)
        convex.topup_account(account)
        account = convex.register_account_name(account_name, account)
    assert(account is not None)
    assert(account.address)
    assert(account.name)
    assert(account.name == account_name)
    assert(convex.resolve_account_name(account_name) == account.address)


def test_account_setup_account(convex_url: str, test_key_pair_info: KeyPairInfo, account_name: str):
    convex = API(convex_url)
    import_key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    account = convex.setup_account(account_name, import_key_pair)
    assert(account is not None)
    assert(account.address)
    assert(account.name)
    assert(account.name == account_name)
    assert(convex.resolve_account_name(account_name) == account.address)
