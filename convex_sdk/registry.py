"""

    ConvexRegistry

"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from convex_sdk.convex import Convex

import logging

from convex_sdk.account import Account

logger = logging.getLogger(__name__)

QUERY_ACCOUNT_ADDRESS = 9


class Registry:
    """
    Reads and writes entries in the Convex Name System (CNS).

    CNS is hierarchical: ``account.alice`` is the entry ``alice`` in the node ``account``, and only the owner
    of a node can create entries in it (see CAD014). Reading works for any name. Writing an entry fails with
    a ``TRUST`` error unless the account owns the parent node.
    """

    def __init__(self, convex: Convex):
        self._convex = convex
        self._address = None
        self._items: dict[str, tuple[int, int | None] | None] = {}

    def is_registered(self, name: str):
        return self.item(name) is not None

    def item(self, name: str):
        """
        Get the ``(address, controller)`` of a CNS entry, or None if the entry does not exist or its value is
        not an address.
        """
        if name not in self._items:
            result = self._convex.query(f'(*registry*/read (symbol "{name}"))', QUERY_ACCOUNT_ADDRESS)
            logger.debug(f'registry read: {result}')
            self._items[name] = None
            record = result.value
            if isinstance(record, (list, tuple)) and len(record) >= 2 and isinstance(record[0], int):
                controller = record[1] if isinstance(record[1], int) else None
                self._items[name] = (record[0], controller)
        return self._items[name]

    def clear(self):
        self._items = {}
        self._address = None

    def register(self, name: str, contract_address: int, account: Account):
        """
        Create the CNS entry ``name`` with the value ``contract_address``, or set the value of an existing
        entry the account controls.

        :raises ConvexAPIError: with code ``TRUST`` if the account may not create or update the entry
        """
        self._convex.transact(f'(*registry*/create (symbol "{name}") #{contract_address})', account)
        self._items.pop(name, None)
        return self.item(name)

    def resolve_owner(self, name: str) -> int | None:
        item = self.item(name)
        if item:
            return item[1]

    def resolve_address(self, name: str) -> int | None:
        item = self.item(name)
        if item:
            return item[0]

    @property
    def address(self) -> int:
        if self._address is None:
            result = self._convex.query('(address *registry*)', QUERY_ACCOUNT_ADDRESS)
            self._registry_address = Account.to_address(result.value)
            logger.debug(f'registry_address: {self._registry_address}')
        return self._registry_address
