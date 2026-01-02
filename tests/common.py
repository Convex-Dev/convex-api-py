"""
Common test utilities and constants.

This module provides shared constants and helper functions for tests.
"""

import logging
import secrets

import pytest

from convex_api.account import Account
from convex_api.convex import Convex
from convex_api.key_pair import KeyPair
from tests.types import KeyPairInfo

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.INFO)

PRIVATE_TEST_KEY = 0x973f69bcd654b264759170724e1e30ccd2e75fc46b7993fd24ce755f0a8c24d0
PUBLIC_KEY = '0x5288Fec4153b702430771DFAC8AeD0B21CAFca4344daE0d47B97F0bf532b3306'
PRIVATE_KEY_MNEMONIC = 'now win hundred protect enroll cram stone come inch ill method often common quiz balance hundred negative truck crime turkey vague ecology nation balcony'   # noqa: E501

PRIVATE_TEST_KEY_TEXT = """
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIGbMFcGCSqGSIb3DQEFDTBKMCkGCSqGSIb3DQEFDDAcBAi3qm1zgjCO5gICCAAw
DAYIKoZIhvcNAgkFADAdBglghkgBZQMEASoEENjvj1nzc0Qy22L+Zi+n7yIEQMLW
o++Jzwlcg3PbW1Y2PxicdFHM3dBOgTWmGsvfZiLhSxTluXTNRCZ8ZLL5pi7JWtCl
JAr4iFzPLkM18YEP2ZE=
-----END ENCRYPTED PRIVATE KEY-----
"""
PRIVATE_TEST_KEY_PASSWORD = 'secret'

CONVEX_URL = 'https://peer.convex.live'

TEST_ACCOUNT_NAME = 'test.convex-api'


def get_convex(url: str | None = None) -> Convex:
    """
    Get a Convex API instance.
    
    :param url: Optional URL for the Convex network. If not provided, uses CONVEX_URL.
    :return: Convex instance
    """
    if url is None:
        url = CONVEX_URL
    return Convex(url)


def get_convex_account(convex: Convex | None = None, key_pair: KeyPair | None = None, url: str | None = None) -> Account:
    """
    Create a new Convex account.
    
    This function creates a new account and skips the test if account creation fails
    (e.g., due to external service unavailability). This ensures that external service
    issues don't break tests that aren't directly testing account creation.
    
    :param convex: Optional API instance. If not provided, creates one using the url.
    :param key_pair: Optional KeyPair to use. If not provided, creates a random one.
    :param url: Optional URL for the Convex network. Only used if convex is not provided.
    :return: Account instance
    :raises: pytest.skip() if account creation fails
    """
    from convex_api.exceptions import ConvexAPIError, ConvexRequestError
    import requests
    
    if convex is None:
        convex = get_convex(url)
    
    if key_pair is None:
        key_pair = KeyPair()
    
    try:
        account = convex.create_account(key_pair)
        return account
    except (ConvexAPIError, ConvexRequestError, requests.RequestException) as e:
        pytest.skip(f"Failed to create account (external service may be unavailable): {e}")


# Pytest fixtures (kept here for backward compatibility, but conftest.py will import them)
@pytest.fixture(scope='module')
def test_key_pair_info() -> KeyPairInfo:
    return {
        'private_hex': PRIVATE_TEST_KEY,
        'private_bytes': KeyPair.to_bytes(PRIVATE_TEST_KEY),
        'private_text': PRIVATE_TEST_KEY_TEXT,
        'private_password': PRIVATE_TEST_KEY_PASSWORD,
        'private_mnemonic': PRIVATE_KEY_MNEMONIC,
        'public_key': PUBLIC_KEY
    }


@pytest.fixture(scope='module')
def test_key_pair(test_key_pair_info: KeyPairInfo):
    key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    return key_pair


@pytest.fixture(scope='module')
def test_account(convex: Convex, test_key_pair: KeyPair):
    from convex_api.exceptions import ConvexAPIError, ConvexRequestError
    import requests
    
    test_account_name = f'{TEST_ACCOUNT_NAME}.{secrets.token_hex(8)}'
    try:
        account = convex.setup_account(test_account_name, test_key_pair)
        if account is not None:
            convex.topup_account(account)
            return account
        else:
            pytest.skip(f"Failed to setup account (account name may already exist or service unavailable)")
    except (ConvexAPIError, ConvexRequestError, requests.RequestException) as e:
        pytest.skip(f"Failed to setup account (external service may be unavailable): {e}")


@pytest.fixture(scope='module')
def convex_url():
    return CONVEX_URL


@pytest.fixture(scope='module')
def convex(convex_url: str):
    return get_convex(convex_url)


@pytest.fixture(scope='module')
def other_account(convex: Convex):
    account = get_convex_account(convex)
    convex.topup_account(account)
    return account

