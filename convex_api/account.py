"""

    Account class for convex api


"""

import re
from typing import Union
from convex_api.key_pair import KeyPair


class Account:

    @staticmethod
    def is_address(text: Union[int, str]) -> bool:
        """
        Returns True if the text value is a valid address.

        :param str, int text: Possible address field.

        :returns: True if the text field is a valid address.

        """
        return Account.to_address(text) >= 0

    @staticmethod
    def to_address(value: Union['Account', int, str]) -> int:
        """
        Convert address text with possible leading '#' to an interger address value.

        :param str text: Address text to convert

        :returns: Integer address

        :raises ValueError: If the address is not valid

        """
        if isinstance(value, Account):
            return value.address
        elif isinstance(value, int):
            return int(value)
        else:
            try:
                address = int(re.sub(r'^#', '', value.strip()))
            except ValueError:
                raise ValueError(f'Invalid address {value}')
            return address

    def __init__(self, key_pair: KeyPair, address: Union['Account', int, str], name: Union[str, None] = None):
        """

        Create a new account with a private key KeyPair.

        :param KeyPair key_pair: The public/private key of the account

        :param int address: address of the account

        :param str name: Optional name of the account

        .. code-block:: python

            >>> # import convex-api
            >>> from convex_api import API, KeyPair, Account

            >>> # setup the network connection
            >>> convex = API('https://convex.world')

            >>> # create a random keypair
            >>> key_pair = KeyPair()

            >>> # create a new account and address
            >>> account = convex.create_account(key_pair)

            >>> # export the private key to a file
            >>> key_pair.export_to_file('/tmp/my_account.pem', 'my secret password')

            >>> # save the address for later
            >>> my_address = account.address

            >>> # ----

            >>> # now import the account and address for later use
            >>> key_pair = KeyPair.import_from_file('/tmp/my_account.pem', 'my secret password')
            >>> account = Account(key_pair, my_address)


        """
        self._key_pair = key_pair
        self._address = Account.to_address(address)
        self._name = name

    def sign(self, hash_text: str) -> str:
        """

        Sign a hash text using the internal key_pair.

        :param str hash_text: Hex string of the hash to sign

        :returns: Hex string of the signed text

        .. code-block:: python

            >>> # create an account
            >>> account = convex.create_account(key_pair)
            >>> # sign a given hash
            >>> sig = account.sign('7e2f1062f5fc51ed65a28b5945b49425aa42df6b7e67107efec357794096e05e')
            >>> print(sig)
            '5d41b964c63d1087ad66e58f4f9d3fe2b7bd0560b..'

        """
        return self._key_pair.sign(hash_text)

    def __str__(self):
        return f'Account {self.address}:{self.key_pair.public_key}'

    @property
    def address(self) -> int:
        """

        :returns: the network account address
        :rtype: int

        .. code-block:: python

            >>> # create an account with the network
            >>> key_pair = KeyPair()
            >>> account = convex.create_account(key_pair)
            >>> print(account.address)
            42

        """
        return self._address

    @address.setter
    def address(self, value: Union['Account', int, str]) -> None:
        """

        Sets the network address of this account

        :param value: Address to use for this account
        :type value: str, int

        .. code-block:: python

            >>> # import the account keys
            >>> key_pair = KeyPair.import_from_mnemonic('my private key words ..')

            >>> account = convex.create_account(key_pair)
            >>> # set the address that was given to us when we created the account on the network
            >>> account.address = 42

        """
        self._address = Account.to_address(value)

    @property
    def name(self) -> Union[str, None]:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def public_key(self) -> bytes:
        """

        Return the public key of the account in the format '0x....'

        :returns: public_key with leading '0x'
        :rtype: str

        .. code-block:: python

            >>> # create an account with the network
            >>> account = convex.create_account(key_pair)

            >>> # show the public key as a hex string
            >>> print(account.public_key)
            0x36d8c5c40dbe2d1b0131acf41c38b9d37ebe04d85...

        """
        return self._key_pair.public_key_bytes

    @property
    def key_pair(self) -> KeyPair:
        """

        Return the internal KeyPair object for this account

        """
        return self._key_pair
