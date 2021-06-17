"""

    Account class for convex api


"""

from convex_api.utils import to_address


class Account:

    def __init__(self, key_pair, address, name=None):
        """

        Create a new account with a private key KeyPair.

        You can also use the following static methods to create an Account object:

            * :meth:`.create`

        :param KeyPair key_pair: The public/private key of the account

        :param int address: address of the account

        :param str name: Optional name of the account

        .. code-block:: python

            >>> # import convex-api
            >>> from convex_api import ConvexAPI, KeyPair, Account

            >>> # setup the network connection
            >>> convex_api = ConvexAPI('https://convex.world')

            >>> # create a random keypair
            >>> key_pair = KeyPair.create()

            >>> # create a new account and address
            >>> account = convex_api.create_account(key_pair)

            >>> # export the private key to a file
            >>> key_pair.export_to_file('/tmp/my_account.pem', 'my secret password')

            >>> # save the address for later
            >>> my_address = account.address

            >>> # ----

            >>> # now import the account and address for later use
            >>> key_pair = KeyPair.import_from_file('/tmp/my_account.pem', 'my secret password')
            >>> account = Account.create(key_pair, my_address)


        """
        self._key_pair = key_pair
        self._address = to_address(address)
        self._name = name

    def sign(self, hash_text):
        """

        Sign a hash text using the internal key_pair.

        :param str hash_text: Hex string of the hash to sign

        :returns: Hex string of the signed text

        .. code-block:: python

            >>> # create an account with no address
            >>> account = Account.create(key_pair)
            >>> # sign a given hash
            >>> sig = account.sign('7e2f1062f5fc51ed65a28b5945b49425aa42df6b7e67107efec357794096e05e')
            >>> print(sig)
            '5d41b964c63d1087ad66e58f4f9d3fe2b7bd0560b..'

        """
        return self._key_pair.sign(hash_text)

    def __str__(self):
        return f'Account {self.address}:{self.key_pair.public_key}'

    @property
    def is_address(self):
        """

        Return true if the address for this account object is set

        :returns: True if this object has a valid address

        """
        return self._address is not None

    @property
    def address(self):
        """

        :returns: the network account address
        :rtype: int

        .. code-block:: python

            >>> # create an account with the network
            >>> account = convex_api.create_account()
            >>> print(account.address)
            42

        """
        return self._address

    @address.setter
    def address(self, value):
        """

        Sets the network address of this account

        :param value: Address to use for this account
        :type value: str, int

        .. code-block:: python

            >>> # import the account keys
            >>> account = Account.import_from_mnemonic('my private key words ..')

            >>> # set the address that was given to us when we created the account on the network
            >>> account.address = 42

        """
        self._address = to_address(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def public_key(self):
        """

        Return the public key of the account in the format '0x....'

        :returns: public_key with leading '0x'
        :rtype: str

        .. code-block:: python

            >>> # create an account with the network
            >>> account = convex_api.create_account(key_pair)

            >>> # show the public key as a hex string
            >>> print(account.public_key)
            0x36d8c5c40dbe2d1b0131acf41c38b9d37ebe04d85...

        """
        return self._key_pair.public_key_bytes

    @property
    def key_pair(self):
        """

        Return the internal KeyPair object for this account

        """
        return self._key_pair

    @staticmethod
    def create(key_pair, address, name=None):
        """

        Create a new account with a random key and an empty address.

        :param KeyPair key_pair: The public/private key of the account

        :param int address: address of the account

        :param str name: Optional name of the account

        :returns: New Account object
        :rtype: Account

        .. code-block:: python

            >>> # create an account with no address
            >>> account = Account.create(key_pair)
            >> account.is_address
            False


        """
        return Account(key_pair, address, name)
