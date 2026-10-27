"""

    Transaction submit must send back the data returned by prepare

"""
import json
from typing import Any
from unittest.mock import patch

from convex_sdk.account import Account
from convex_sdk.convex import Convex
from convex_sdk.key_pair import KeyPair

HASH = 'd003ea0d110281031102110132012b'
ADDRESS = 13


class FakeResponse:
    status_code = 200

    def __init__(self, body: dict[str, Any]):
        self._body = body
        self.text = json.dumps(body)

    def json(self) -> dict[str, Any]:
        return self._body


def transact_with_prepare_response(prepare_body: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Run `transact` against a fake peer and return the (url, JSON body) of each request it made."""
    requests_made: list[tuple[str, dict[str, Any]]] = []

    def fake_post(url: str, data: str) -> FakeResponse:
        requests_made.append((url, json.loads(data)))
        if url.endswith('/transaction/prepare'):
            return FakeResponse(prepare_body)
        return FakeResponse({'value': 3})

    account = Account(KeyPair(), ADDRESS)
    with patch('convex_sdk.convex.requests.post', side_effect=fake_post):
        result = Convex('http://localhost:8080').transact('(+ 1 2)', account)
    assert result.value == 3
    return requests_made


def test_submit_sends_prepare_data():
    requests_made = transact_with_prepare_response({
        'address': ADDRESS,
        'hash': HASH,
        'data': HASH,
        'sequence': 2,
        'source': '(+ 1 2)'
    })
    assert [url for url, _ in requests_made] == [
        'http://localhost:8080/api/v1/transaction/prepare',
        'http://localhost:8080/api/v1/transaction/submit'
    ]
    submit = requests_made[1][1]
    assert submit['data'] == HASH
    assert submit['hash'] == HASH
    assert submit['address'] == ADDRESS


def test_submit_omits_data_when_peer_returns_none():
    requests_made = transact_with_prepare_response({
        'address': ADDRESS,
        'hash': HASH,
        'sequence': 2,
        'source': '(+ 1 2)'
    })
    submit = requests_made[1][1]
    assert 'data' not in submit
    assert submit['hash'] == HASH


def test_unset_request_fields_are_not_sent():
    requests_made = transact_with_prepare_response({
        'address': ADDRESS,
        'hash': HASH,
        'data': HASH,
        'sequence': 2,
        'source': '(+ 1 2)'
    })
    prepare = requests_made[0][1]
    assert prepare == {'address': ADDRESS, 'source': '(+ 1 2)'}
