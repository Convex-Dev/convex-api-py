"""

    Test Convex api

"""
import pytest
import secrets

from convex_api.account import Account
from convex_api.api import API
from convex_api.key_pair import KeyPair
from convex_api.exceptions import (
    ConvexRequestError
)

TEST_FUNDING_AMOUNT = 8888888


def test_convex_api_request_funds(convex_url: str, test_account: Account):
    convex = API(convex_url)
    amount = secrets.randbelow(100) + 1
    request_amount = convex.request_funds(amount, test_account)
    assert(request_amount == amount)

def test_convex_api_topup_account(convex_url: str):
    convex = API(convex_url)
    key_pair = KeyPair()
    account = convex.create_account(key_pair)
    topup_amount = TEST_FUNDING_AMOUNT
    amount = convex.topup_account(account, topup_amount)
    assert(amount >= topup_amount)

    account = convex.create_account(key_pair)
    amount = convex.topup_account(account)
    assert(amount >= 0)

def test_convex_get_account_info(convex_url: str, test_account: Account):
    convex = API(convex_url)
    info = convex.get_account_info(test_account)
    assert(info)
    assert(info.type == 'user')
    assert(info.balance > 0)
    assert(info.sequence >= 0)

    with pytest.raises(ConvexRequestError, match='INCORRECT'):
        info = convex.get_account_info(pow(2, 100))

    with pytest.raises(ConvexRequestError, match='INCORRECT'):
        info = convex.get_account_info(pow(2, 1024))

    key_pair = KeyPair()
    account = convex.create_account(key_pair)
    request_amount = convex.request_funds(TEST_FUNDING_AMOUNT, account)
    assert(request_amount == TEST_FUNDING_AMOUNT)
    info = convex.get_account_info(account)
    assert(info)
    assert(info.balance == TEST_FUNDING_AMOUNT)

def test_convex_account_name_registry(convex_url: str, test_account: Account, test_key_pair: KeyPair):
    account_name = f'test.convex-api.{secrets.token_hex(4)}'
    convex = API(convex_url)

    address = convex.resolve_account_name(account_name)
    assert(not address)

    account = convex.load_account(account_name, test_key_pair)
    assert(not account)


    register_account = convex.register_account_name(account_name, test_account)
    assert(register_account.address == test_account.address)

    assert(convex.resolve_account_name(account_name) == test_account.address)

    new_account = convex.create_account(test_key_pair)
    register_account = convex.register_account_name(account_name, new_account, test_account)

    assert(register_account.address == new_account.address)
    assert(convex.resolve_account_name(account_name) == new_account.address)

    # clear the cache in the registry
    convex.registry.clear()
    assert(convex.resolve_account_name(account_name) == new_account.address)


def test_convex_resolve_name(convex_url: str):
    convex = API(convex_url)
    address = convex.resolve_name('convex.trust')
    assert(address)


def test_convex_transfer_account(convex_url: str, test_account: Account):
    convex = API(convex_url)

    # create a new account with a random keys
    key_pair = KeyPair()
    account_1 = convex.create_account(key_pair)
    convex.topup_account(account_1)
    result = convex.send('(map inc [1 2 3 4 5])', account_1)
    assert(result is not None)
    assert 'value' in result.dict()
    assert(result.value == [2, 3, 4, 5, 6])

    # transfer the new account_1 to use the same keys as the test_account
    account_1_change = convex.transfer_account(test_account, account_1)
    assert(account_1_change)
    # public key should be the same as the test_account
    assert(account_1_change.key_pair.is_equal(test_account.key_pair))
    # adress still the same
    assert(account_1_change.address == account_1.address )

    # test out new key
    result = convex.send('(map inc [1 2 3 4 5])', account_1_change)
    assert(result is not None)
    assert 'value' in result.dict()
    assert(result.value == [2, 3, 4, 5, 6])


def test_convex_api_send_basic_lisp(convex_url: str, test_account: Account):
    convex = API(convex_url)
    request_amount = convex.request_funds(TEST_FUNDING_AMOUNT, test_account)
    assert(request_amount == TEST_FUNDING_AMOUNT)
    result = convex.send('(map inc [1 2 3 4 5])', test_account)
    assert(result is not None)
    assert 'value' in result.dict()
    assert(result.value == [2, 3, 4, 5, 6])

def test_convex_api_get_balance_no_funds(convex_url: str):
    convex = API(convex_url)
    key_pair = KeyPair()
    account = convex.create_account(key_pair)
    new_balance = convex.get_balance(account)
    assert(new_balance == 0)

def test_convex_api_get_balance_small_funds(convex_url: str, test_account: Account):
    convex = API(convex_url)
    key_pair = KeyPair()
    account = convex.create_account(key_pair)
    amount = 100
    request_amount = convex.request_funds(amount, account)
    assert(request_amount == amount)
    new_balance = convex.get_balance(account)
    assert(new_balance == amount)

def test_convex_api_get_balance_new_account(convex_url: str):
    convex = API(convex_url)
    key_pair = KeyPair()
    account = convex.create_account(key_pair)
    amount = TEST_FUNDING_AMOUNT
    request_amount = convex.request_funds(amount, account)
    assert(request_amount == amount)
    new_balance = convex.get_balance(account)
    assert(new_balance == TEST_FUNDING_AMOUNT)

def test_convex_api_call(convex_url: str):

    deploy_storage = """
(def storage-example
    (deploy
        '(do
            (def stored-data
                ^{:private? true}
                nil
            )
            (defn get
                ^{:callable? true}
                []
                stored-data
            )
            (defn set
                ^{:callable? true}
                [x]
                ( def stored-data x)
            )
        )
    )
)
"""
    convex = API(convex_url)
    key_pair = KeyPair()
    account = convex.create_account(key_pair)
    amount = TEST_FUNDING_AMOUNT
    request_amount = convex.request_funds(amount, account)
    assert(request_amount == amount)
    result = convex.send(deploy_storage, account)
    assert(result is not None)
    contract_address = Account.to_address(result.value)
    assert(contract_address)
    test_number = secrets.randbelow(1000)
    call_set_result = convex.send(f'(call storage-example(set {test_number}))', account)
    assert(call_set_result is not None)
    assert(call_set_result.value == test_number)
    call_get_result = convex.query('(call storage-example(get))', account)
    assert(call_get_result is not None)
    assert(call_get_result.value == test_number)

    # now api calls using language scrypt
    """
    convex = API(convex_url, API.LANGUAGE_SCRYPT)
    test_number = secrets.randbelow(1000)
    call_set_result = convex.send(f'call storage_example set({test_number})', account)
    assert(call_set_result['value'] == test_number)

    call_get_result = convex.query('call storage_example get()', account)
    assert(call_get_result['value'] == test_number)

    call_get_result = convex.query(f'call {contract_address} get()', account)
    assert(call_get_result['value'] == test_number)

    with pytest.raises(ConvexRequestError, match='400'):
        call_set_result = convex.send(f'call {contract_address}.set({test_number})', account)

    address = convex.get_address('storage_example', account)
    assert(address == contract_address)
    """
def test_convex_api_transfer(convex_url: str):
    convex = API(convex_url)
    key_pair = KeyPair()
    account_from = convex.create_account(key_pair)
    account_to = convex.create_account(key_pair)
    amount = TEST_FUNDING_AMOUNT
    request_amount = convex.request_funds(amount, account_from)
    assert(request_amount == amount)

    transfer_amount = int(amount / 2)
    result = convex.transfer(account_to, transfer_amount, account_from)
    assert(result)
    assert(result == transfer_amount)
    #balance_from = convex.get_balance(account_from)
    balance_to = convex.get_balance(account_to)
    assert(balance_to == transfer_amount)

def test_convex_api_query_lisp(convex_url: str, test_account: Account):
    convex = API(convex_url)
    result = convex.query(f'(address {test_account.address})', test_account)
    assert(result is not None)
    # return value is the address as a checksum
    assert(Account.to_address(result.value) == test_account.address)
