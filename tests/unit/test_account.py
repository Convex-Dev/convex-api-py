"""

    Test Account class

"""
import secrets

import pytest


from convex_api.account import Account
from convex_api.key_pair import KeyPair



def test_account_create_new():
    key_pair = KeyPair()
    account = Account(key_pair, 99)
    assert(account)
    assert(account.public_key)

def test_account_is_address():
    address_int = secrets.randbelow(pow(2, 1024)) + 1
    assert(Account.is_address(address_int))

    address_str = str(address_int)
    assert(Account.is_address(address_str))

    address = Account.to_address(f'#{address_str}')
    assert(address == address_int)

    with pytest.raises(ValueError):
        Account.is_address('test')

    with pytest.raises(ValueError):
        Account.is_address(' #')

    assert(Account.is_address('#0'))

    assert(not Account.is_address('#-1'))
