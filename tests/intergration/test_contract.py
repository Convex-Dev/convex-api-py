"""

    Test contract

"""
import pytest  # type: ignore # noqa: F401

from convex_api import (
    Account,
    API,
    Contract
)


TEST_FUNDING_AMOUNT = 8888888

TEST_CONTRACT_FILENAME = './tests/resources/test_contract.cvx'
TEST_CONTRACT_NAME = 'test_contract_starfish'


def test_convex_api_deploy_contract(convex_url: str, test_account: Account):
    convex = API(convex_url)

    # create a contract object
    contract = Contract(convex)

    # set the default owner to the test_account
    owner_account = test_account

    # see if it has already been created by another test account
    owner_address = contract.resolve_owner_address(TEST_CONTRACT_NAME)
    if owner_address:
        # if so then rebuild the owner account using the same key_pair
        owner_account = Account(test_account.key_pair, owner_address)
        # and topup the account to avoid out of juice errors
        convex.topup_account(owner_account, TEST_FUNDING_AMOUNT)
    else:
        owner_address = test_account.address

    # deploy the contract
    contract_address = contract.deploy(owner_account, filename=TEST_CONTRACT_FILENAME, name=TEST_CONTRACT_NAME)
    assert(contract_address)
    # load the contract - should be the same address
    new_address = contract.load(TEST_CONTRACT_NAME)
    assert(contract_address == new_address)
    assert(contract_address == contract.address)
    assert(owner_address == contract.owner_address)


    contract = convex.load_contract(TEST_CONTRACT_NAME)
    assert(contract)
    assert(contract_address == contract.address)


def test_convex_api_contract_escape_string():
    test_text = 'this is a test "string" '
    assert('this is a test \\"string\\" ' == Contract.escape_string(test_text))
