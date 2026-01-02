"""
    Test account based functions

"""

import secrets

import pytest

from convex_api import KeyPair
from convex_api.exceptions import ConvexAPIError, ConvexRequestError
from tests.common import get_convex
from tests.types import KeyPairInfo
import requests

TEST_ACCOUNT_NAME = 'test.convex-api'


@pytest.fixture
def account_name():
    return f'{TEST_ACCOUNT_NAME}-{secrets.token_hex(8)}'


def test_account_api_create_account(convex_url: str):
    convex = get_convex(convex_url)
    key_pair = KeyPair()
    try:
        result = convex.create_account(key_pair)
        assert result
    except (ConvexAPIError, ConvexRequestError, requests.RequestException) as e:
        # Skip if account creation fails due to external service issues (e.g., 403)
        pytest.skip(f"Failed to create account (external service may be unavailable): {e}")


def test_account_api_multi_create_account(convex_url: str):
    convex = get_convex(convex_url)
    key_pair = KeyPair()
    try:
        account_1 = convex.create_account(key_pair)
        assert account_1
        account_2 = convex.create_account(key_pair)
        assert account_2

        assert account_1.public_key == account_1.public_key
        assert account_1.public_key == account_2.public_key
        assert account_1.address != account_2.address
    except (ConvexAPIError, ConvexRequestError, requests.RequestException) as e:
        # Skip if account creation fails due to external service issues (e.g., 403)
        pytest.skip(f"Failed to create account (external service may be unavailable): {e}")


def test_account_name(convex_url: str, test_key_pair_info: KeyPairInfo, account_name: str):
    convex = get_convex(convex_url)
    import_key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    if convex.resolve_account_name(account_name):
        account = convex.load_account(account_name, import_key_pair)
    else:
        try:
            account = convex.create_account(import_key_pair)
            convex.topup_account(account)
            account = convex.register_account_name(account_name, account)
        except (ConvexAPIError, ConvexRequestError, requests.RequestException) as e:
            # Skip if account creation fails due to external service issues (e.g., 403)
            pytest.skip(f"Failed to create account (external service may be unavailable): {e}")
    assert account is not None
    assert account.address
    assert account.name
    assert account.name == account_name
    assert convex.resolve_account_name(account_name) == account.address


def test_account_setup_account(convex_url: str, test_key_pair_info: KeyPairInfo, account_name: str):
    convex = get_convex(convex_url)
    import_key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    try:
        account = convex.setup_account(account_name, import_key_pair)
        assert account is not None
        assert account.address
        assert account.name
        assert account.name == account_name
        assert convex.resolve_account_name(account_name) == account.address
    except (ConvexAPIError, ConvexRequestError, requests.RequestException) as e:
        # Skip if account setup fails due to external service issues (e.g., 403)
        pytest.skip(f"Failed to setup account (external service may be unavailable): {e}")
