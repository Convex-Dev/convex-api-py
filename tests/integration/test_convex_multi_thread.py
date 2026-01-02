"""

    Test Convex multi thread

"""
import secrets
from multiprocessing import (
    Process,
    Value
)
from typing import Any

import pytest  # type: ignore # noqa: F401

from convex_api.account import Account
from convex_api.exceptions import ConvexAPIError, ConvexRequestError
from convex_api.key_pair import KeyPair
from tests.common import get_convex, get_convex_account
import requests
import pytest

TEST_FUNDING_AMOUNT = 8000000


def process_on_convex(convex: API, test_account: Account, result_value: Any):
    values: list[str] = []
    inc_values: list[int] = []
    for _ in range(0, 4):
        for _ in range(secrets.randbelow(10) + 1):
            value = secrets.randbelow(1000)
            values.append(str(value))
            inc_values.append(value + 1)
            value_text = " ".join(values)
        result = convex.send(f'(map inc [{value_text}])', test_account, sequence_retry_count=100)  # type: ignore
        assert result is not None
        assert result.value == inc_values
    result_value.value = 1  # type: ignore


def test_convex_api_multi_thread_send(convex_url: str, test_account: Account):

    process_count = 4
    convex = get_convex(convex_url)
    convex.topup_account(test_account)
    process_items: dict[int, dict[str, Any]] = {}
    for index in range(process_count):
        result_value = Value('i', 0)
        proc = Process(target=process_on_convex, args=(convex, test_account, result_value))
        process_items[index] = {
            'process': proc,
            'result_value': result_value
        }
        proc.start()

    for index, process_item in process_items.items():
        process_item['process'].join()
        assert process_item['result_value'].value == 1


def process_convex_account_creation(convex: API, result_value: Any):
    key_pair = KeyPair()
    account = convex.create_account(key_pair)
    assert account
    assert account.address
    result_value.value = 1  # type: ignore


def test_convex_api_multi_thread_account_creation(convex_url: str):
    # First check if account creation is available by trying to create one account
    # If it fails, skip the entire test since multiprocessing can't use pytest.skip()
    convex = get_convex(convex_url)
    try:
        test_key_pair = KeyPair()
        test_account = convex.create_account(test_key_pair)
        assert test_account is not None
    except (ConvexAPIError, ConvexRequestError, requests.RequestException) as e:
        pytest.skip(f"Account creation not available (external service may be unavailable): {e}")
    
    # If we get here, account creation works, so proceed with multiprocessing test
    process_count = 20
    process_items: dict[int, dict[str, Any]] = {}
    for index in range(process_count):
        result_value = Value('i', 0)
        proc = Process(target=process_convex_account_creation, args=(convex, result_value))
        process_items[index] = {
            'process': proc,
            'result_value': result_value
        }
        proc.start()

    for index, process_item in process_items.items():
        process_item['process'].join()
        assert process_item['result_value'].value == 1


def process_convex_deploy(convex: API, result_value: Any):
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
                (def stored-data x)
            )
        )
    )
)
"""
    key_pair = KeyPair()
    account = convex.create_account(key_pair)
    for _ in range(0, 10):
        convex.topup_account(account)
        try:
            result = convex.send(deploy_storage, account)
        except ConvexAPIError as e:
            balance = convex.get_balance(account)
            print('*' * 132)
            print('failed send', e, balance)
            print('*' * 132)
            result_value.value = balance  # type: ignore
            return
        assert result is not None
        assert result.value
        contract_address = Account.to_address(result.value)
        assert contract_address
    result_value.value = 1  # type: ignore


def test_convex_api_multi_thread_deploy(convex_url: str):
    process_count = 10
    convex = get_convex(convex_url)
    account = get_convex_account(convex)
    convex.request_funds(TEST_FUNDING_AMOUNT, account)
    process_items: dict[int, dict[str, Any]] = {}
    for index in range(process_count):
        result_value = Value('i', 0)
        proc = Process(target=process_convex_deploy, args=(convex, result_value))
        process_items[index] = {
            'process': proc,
            'result_value': result_value
        }
        proc.start()

    for index, process_item in process_items.items():
        process_item['process'].join()
        assert process_item['result_value'].value == 1
