"""

    Test Convex api

"""
import secrets

import pytest

from convex_sdk.account import Account
from convex_sdk.exceptions import ConvexRequestError
from convex_sdk.key_pair import KeyPair
from tests.common import get_convex, get_convex_account

TEST_FUNDING_AMOUNT = 8888888


def test_convex_sdk_request_funds(convex_url: str, test_account: Account):
    convex = get_convex(convex_url)
    amount = secrets.randbelow(100) + 1
    request_amount = convex.request_funds(amount, test_account)
    assert request_amount == amount


def test_convex_sdk_topup_account(convex_url: str):
    convex = get_convex(convex_url)
    account = get_convex_account(convex)
    topup_amount = TEST_FUNDING_AMOUNT
    amount = convex.topup_account(account, topup_amount)
    assert amount >= topup_amount

    account = get_convex_account(convex)
    amount = convex.topup_account(account)
    assert amount >= 0


def test_convex_get_account_info(convex_url: str, test_account: Account):
    convex = get_convex(convex_url)
    info = convex.get_account_info(test_account)
    assert info
    assert info.type == 'user'
    assert info.balance > 0
    assert info.sequence >= 0

    with pytest.raises(ConvexRequestError, match='INCORRECT'):
        info = convex.get_account_info(pow(2, 100))

    with pytest.raises(ConvexRequestError, match='INCORRECT'):
        info = convex.get_account_info(pow(2, 1024))

    account = get_convex_account(convex)
    request_amount = convex.request_funds(TEST_FUNDING_AMOUNT, account)
    assert request_amount == TEST_FUNDING_AMOUNT
    info = convex.get_account_info(account)
    assert info
    assert info.balance == TEST_FUNDING_AMOUNT


def test_convex_account_name_registry(convex_url: str, test_account: Account, test_key_pair: KeyPair):
    account_name = f'test.convex-api.{secrets.token_hex(4)}'
    convex = get_convex(convex_url)

    address = convex.resolve_account_name(account_name)
    assert not address

    account = convex.load_account(account_name, test_key_pair)
    assert not account

    register_account = convex.register_account_name(account_name, test_account)
    assert register_account.address == test_account.address

    assert convex.resolve_account_name(account_name) == test_account.address

    # This test is testing transfer_account, not create_account directly
    # Use get_convex_account to handle failures gracefully
    new_account = get_convex_account(convex, test_key_pair)
    register_account = convex.register_account_name(account_name, new_account, test_account)

    assert register_account.address == new_account.address
    assert convex.resolve_account_name(account_name) == new_account.address

    # clear the cache in the registry
    convex.registry.clear()
    assert convex.resolve_account_name(account_name) == new_account.address


def test_convex_resolve_name(convex_url: str):
    convex = get_convex(convex_url)
    address = convex.resolve_name('convex.trust')
    assert address


def test_convex_transfer_account(convex_url: str, test_account: Account):
    convex = get_convex(convex_url)

    # create a new account with a random keys
    account_1 = get_convex_account(convex)
    convex.topup_account(account_1)
    result = convex.transact('(map inc [1 2 3 4 5])', account_1)
    assert result is not None
    assert 'value' in result.model_dump()
    assert result.value == [2, 3, 4, 5, 6]

    # transfer the new account_1 to use the same keys as the test_account
    account_1_change = convex.transfer_account(test_account, account_1)
    assert account_1_change
    # public key should be the same as the test_account
    assert account_1_change.key_pair.is_equal(test_account.key_pair)
    # adress still the same
    assert account_1_change.address == account_1.address

    # test out new key
    result = convex.transact('(map inc [1 2 3 4 5])', account_1_change)
    assert result is not None
    assert 'value' in result.model_dump()
    assert result.value == [2, 3, 4, 5, 6]


def test_convex_sdk_send_basic_lisp(convex_url: str, test_account: Account):
    convex = get_convex(convex_url)
    request_amount = convex.request_funds(TEST_FUNDING_AMOUNT, test_account)
    assert request_amount == TEST_FUNDING_AMOUNT
    result = convex.transact('(map inc [1 2 3 4 5])', test_account)
    assert result is not None
    assert 'value' in result.model_dump()
    assert result.value == [2, 3, 4, 5, 6]


def test_convex_sdk_get_balance_no_funds(convex_url: str):
    convex = get_convex(convex_url)
    account = get_convex_account(convex)
    new_balance = convex.get_balance(account)
    assert new_balance == 0


def test_convex_sdk_get_balance_small_funds(convex_url: str, test_account: Account):
    convex = get_convex(convex_url)
    account = get_convex_account(convex)
    amount = 100
    request_amount = convex.request_funds(amount, account)
    assert request_amount == amount
    new_balance = convex.get_balance(account)
    assert new_balance == amount


def test_convex_sdk_get_balance_new_account(convex_url: str):
    convex = get_convex(convex_url)
    account = get_convex_account(convex)
    amount = TEST_FUNDING_AMOUNT
    request_amount = convex.request_funds(amount, account)
    assert request_amount == amount
    new_balance = convex.get_balance(account)
    assert new_balance == TEST_FUNDING_AMOUNT


def test_convex_sdk_call(convex_url: str):

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
    convex = get_convex(convex_url)
    account = get_convex_account(convex)
    amount = TEST_FUNDING_AMOUNT
    request_amount = convex.request_funds(amount, account)
    assert request_amount == amount
    result = convex.transact(deploy_storage, account)
    assert result is not None
    contract_address = Account.to_address(result.value)
    assert contract_address
    test_number = secrets.randbelow(1000)
    call_set_result = convex.transact(f'(call storage-example(set {test_number}))', account)
    assert call_set_result is not None
    assert call_set_result.value == test_number
    call_get_result = convex.query('(call storage-example(get))', account)
    assert call_get_result is not None
    assert call_get_result.value == test_number

    # now api calls using language scrypt
    """
    convex = get_convex(convex_url)
    # Note: LANGUAGE_SCRYPT support may need to be added to get_convex if needed
    test_number = secrets.randbelow(1000)
    call_set_result = convex.transact(f'call storage_example set({test_number})', account)
    assert call_set_result['value'] == test_number

    call_get_result = convex.query('call storage_example get()', account)
    assert call_get_result['value'] == test_number

    call_get_result = convex.query(f'call {contract_address} get()', account)
    assert call_get_result['value'] == test_number

    with pytest.raises(ConvexRequestError, match='400'):
        call_set_result = convex.transact(f'call {contract_address}.set({test_number})', account)

    address = convex.get_address('storage_example', account)
    assert address == contract_address
    """


def test_convex_sdk_transfer(convex_url: str):
    convex = get_convex(convex_url)
    account_from = get_convex_account(convex)
    account_to = get_convex_account(convex)
    amount = TEST_FUNDING_AMOUNT
    request_amount = convex.request_funds(amount, account_from)
    assert request_amount == amount

    transfer_amount = int(amount / 2)
    result = convex.transfer(account_to, transfer_amount, account_from)
    assert result
    assert result == transfer_amount
    # balance_from = convex.get_balance(account_from)
    balance_to = convex.get_balance(account_to)
    assert balance_to == transfer_amount


def test_convex_sdk_query_lisp(convex_url: str, test_account: Account):
    convex = get_convex(convex_url)
    result = convex.query(f'(address {test_account.address})', test_account)
    assert result is not None
    # return value is the address as a checksum
    assert Account.to_address(result.value) == test_account.address
