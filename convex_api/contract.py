"""


Convex Contract

"""

import re

from convex_api.utils import to_address


class Contract:
    def __init__(self, convex):
        """

        Contract class to provide access and name resolution to deployed convex contracts.

        """
        self._convex = convex
        self._name = None
        self._address = None
        self._owner_address = None

    def load(self, name=None, address=None, owner_address=None):
        """

        Load a contract details using it's registered name or directly using it's known address.

        :param str name: Name of the contract that has been registered.
        If provided the address and owner_address of the registration is stored within this object

        :param str, int, Account address: Address of the contract, if the name is not known,
        then you can provide the actual address of the contract.

        :param str, int, Account owner_address: If the contract is registered the owner address of the resgistration.

        :returns int The address of the resolved contract

        """
        if name:
            address = self.resolve_address(name)
            owner_address = self.resolve_owner_address(name)
            self._name = name

        if address is None:
            raise ValueError('no contract found')

        if owner_address is None:
            owner_address = address

        self._address = to_address(address)
        self._owner_address = to_address(owner_address)
        return self._address

    def deploy(self, account, text=None, filename=None, name=None, owner_account=None):
        """

        Deploy a new/updated contract on the convex network.

        :param Account account: Account to use to deploy the contract

        :param str text: Contract text to deploy

        :param str filename: Filename of the contract to deploy

        :param str name: Name of the contract to register

        :param Account onwer_account: Optional owner account of the registration.
        If not provided then the Account will be used.

        :returns Address of the new contract

        """
        if filename:
            with open(filename, 'r') as fp:
                text = fp.read()
        if text is None:
            raise ValueError('You need to provide a contract filename or text to deploy')
        deploy_line = f"""
(deploy
    (quote
        (do
            {text}
        )
    )
)
    """
        result = self._convex.send(deploy_line, account)
        if result and 'value' in result:
            address = to_address(result["value"])
            if name:
                if owner_account is None:
                    owner_account = account
                self._convex.registry.register(name, address, owner_account)
            return address

    def register_contract_name(self, name, address, account):
        """

        Register a contract address with a resolvable name. This name can be used on the Convex network to resolve
        to the contract address.

        :param str name: Name to register.

        :param str, int, Account address: Address to use to assign with the name.

        :param Account account: Account who owns the registration.

        :returns Result from the register transaction

        """
        return self._convex.registry.register(name, address, account)

    def send(self, transaction, account):
        """

        Sends a contract transaction to the contract. You need to run `load` before calling this method.

        :param str transaction: Transaction to send to the contract.

        :param Account account: Account to pay for the transaction.

        :returns The transaction result.

        """
        if not self._address:
            raise ValueError(f'No contract address found for {self._name}')
        return self._convex.send(f'(call #{self._address} {transaction})', account)

    def query(self, transaction, account_address=None):
        """

        Sends a query to the contract.

        :param str transaction: The transaction query to send to the contract

        :param str, int, Account account_address: The address to provide as the sender for this query.

        :returns The query result

        """
        if not self._address:
            raise ValueError(f'No contract address found for {self._name}')
        if account_address is None:
            account_address = to_address(account_address)
        if account_address is None:
            account_address = self._address
        return self._convex.query(f'(call #{self._address} {transaction})', account_address)

    def resolve_address(self, name):
        """

        Return an address from a registered name.

        """
        return self._convex.registry.resolve_address(name)

    def resolve_owner_address(self, name):
        """

        Returns the register owner of a registered name.

        """
        return self._convex.registry.resolve_owner(name)

    @property
    def is_registered(self):
        return self._address is not None

    @property
    def address(self):
        return self._address

    @property
    def owner_address(self):
        return self._owner_address

    @property
    def name(self):
        return self._name

    @staticmethod
    def escape_string(text):
        """
        Escape any string and replace quote chars with leading escape chars

        """
        escape_text = re.sub('\\\\', '\\\\\\\\', text)
        escape_text = re.sub('"', '\\"', escape_text)
        return escape_text