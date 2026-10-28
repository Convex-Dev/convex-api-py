"""

    Registry reads and writes entries of the hierarchical Convex Name System

"""
from typing import (
    Any,
    cast
)

from convex_sdk.account import Account
from convex_sdk.convex import Convex
from convex_sdk.key_pair import KeyPair
from convex_sdk.registry import (
    QUERY_ACCOUNT_ADDRESS,
    Registry
)


class FakeResult:
    def __init__(self, value: Any):
        self.value = value


class FakeConvex:
    """Records the queries and transactions the registry sends, and answers queries from `records`."""

    def __init__(self, records: dict[str, Any]):
        self.records = records
        self.queries: list[tuple[str, int]] = []
        self.transactions: list[str] = []

    def query(self, source: str, address: int) -> FakeResult:
        self.queries.append((source, address))
        name = source.split('"')[1]
        return FakeResult(self.records.get(name))

    def transact(self, source: str, account: Account) -> FakeResult:
        self.transactions.append(source)
        return FakeResult(None)


def registry_for(records: dict[str, Any]) -> tuple[Registry, FakeConvex]:
    fake = FakeConvex(records)
    return Registry(cast(Convex, fake)), fake


def test_item_reads_value_and_controller():
    registry, fake = registry_for({'convex.trust': [10, 6, None, [9, ['convex', 'trust']]]})
    assert registry.item('convex.trust') == (10, 6)
    assert registry.resolve_address('convex.trust') == 10
    assert registry.resolve_owner('convex.trust') == 6
    assert fake.queries == [('(*registry*/read (symbol "convex.trust"))', QUERY_ACCOUNT_ADDRESS)]


def test_item_is_cached_until_cleared():
    registry, fake = registry_for({'convex.trust': [10, 6, None, None]})
    registry.item('convex.trust')
    registry.item('convex.trust')
    assert len(fake.queries) == 1
    registry.clear()
    registry.item('convex.trust')
    assert len(fake.queries) == 2


def test_missing_entry_is_none():
    registry, _ = registry_for({})
    assert registry.item('account.nobody') is None
    assert not registry.is_registered('account.nobody')
    assert registry.resolve_address('account.nobody') is None


def test_entry_whose_value_is_not_an_address_is_none():
    registry, _ = registry_for({'convex.node': [None, 6, None, [9, ['convex']]]})
    assert registry.item('convex.node') is None


def test_controller_that_is_not_an_address_is_none():
    registry, _ = registry_for({'account.alice': [12, [9, ['monitor']], None, None]})
    assert registry.item('account.alice') == (12, None)


def test_register_creates_entry_and_returns_it():
    registry, fake = registry_for({})
    account = Account(KeyPair(), 12)
    fake.records['account.alice'] = [12, 12, None, None]
    item = registry.register('account.alice', 12, account)
    assert fake.transactions == ['(*registry*/create (symbol "account.alice") #12)']
    assert item == (12, 12)


def test_register_does_not_return_a_cached_old_value():
    registry, fake = registry_for({'account.alice': [11, 12, None, None]})
    assert registry.item('account.alice') == (11, 12)
    fake.records['account.alice'] = [13, 12, None, None]
    assert registry.register('account.alice', 13, Account(KeyPair(), 12)) == (13, 12)
