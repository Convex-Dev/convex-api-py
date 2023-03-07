"""

    KeyPair class for convex api


"""

from typing import Union
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


from mnemonic import Mnemonic

from convex_api.utils import (
    remove_0x_prefix,
    to_bytes,
    to_hex,
    to_public_key_checksum
)


class KeyPair:

    def __init__(self, private_key: Union[Ed25519PrivateKey, None] = None):
        """

        Create a new keypair object with a public and private key as a Ed25519PrivateKey. It is better to use
        one of the following static methods to create an KeyPair object:

            * :meth:`import_from_bytes`
            * :meth:`import_from_file`
            * :meth:`import_from_mnemonic`
            * :meth:`import_from_text`

        :param Ed25519PrivateKey private_key: The public/private key as an Ed25519PrivateKey object


        The Convex KeyPair class, contains the public/private keys.

        To re-use the KeyPair again, you can import the keys.

        **Note**
        For security reasons all of the keys and password text displayed below in the documentation
        are only truncated ending with a **`...`**

        .. code-block:: python

            >>> # import convex-api
            >>> from convex_api import ConvexAPI

            >>> # setup the network connection
            >>> convex_api = ConvexAPI('https://convex.world')

        """
        if private_key is None:
            private_key = Ed25519PrivateKey.generate()
        self._private_key = private_key
        self._public_key = private_key.public_key()

    def sign(self, hash_text: str) -> Union[str, None]:
        """

        Sign a hash text using the private key.

        :param str hash_text: Hex string of the hash to sign

        :returns: Hex string of the signed text

        .. code-block:: python

            >>> sig = key_pair.sign('7e2f1062f5fc51ed65a28b5945b49425aa42df6b7e67107efec357794096e05e')
            >>> print(sig)
            '5d41b964c63d1087ad66e58f4f9d3fe2b7bd0560b..'

        """
        hash_data = to_bytes(hexstr=hash_text)
        if not hash_data:
            return None
        signed_hash_bytes = self._private_key.sign(hash_data)
        return to_hex(signed_hash_bytes)

    def export_to_text(self, password: Union[str, bytes]):
        """

        Export the private key to an encrypted PEM string.

        :param str password: Password to encrypt the private key value

        :returns: The private key as a PEM formated encrypted string

        .. code-block:: python

            >>> # create a keypair
            >>> key_pair = KeyPair()

            >>> # export the private key for later use
            >>> print(key_pair.export_to_text('secret password'))
            -----BEGIN ENCRYPTED PRIVATE KEY-----
            MIGbMFcGCSqGSIb3DQEFDTBKMCkGCSqGSIb3DQEFDDAcBAhKG+LC3hJoJQICCAAw
            DAYIKoZIhvcNAgkFAD ...


        """
        if isinstance(password, str):
            password = password.encode()
        private_data = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password)
        )
        return private_data.decode()

    @property
    def export_to_mnemonic(self):
        """

        Export the private key as a mnemonic words. You must keep this secret since the private key can be
        recreated using the words.

        :returns: mnemonic word list of the private key

        .. code-block:: python

            >>> # create a keypair
            >>> key_pair = KeyPair()

            >>> # export the private key for later use
            >>> print(key_pair.export_to_mnemonic())
            grief stuff resemble dry frozen exercise ...

        """
        mnemonic = Mnemonic('english')
        return mnemonic.to_mnemonic(self._private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ))

    def export_to_file(self, filename: str, password: Union[str, bytes]) -> None:
        """

        Export the private key to a file. This uses `export_to_text` to export as a string.
        Then saves this in a file.

        :param str filename: Filename to create with the PEM string

        :param str password: Password to use to encypt the private key

        .. code-block:: python

            >>> # create a keypair
            >>> key_pair = KeyPair()

            >>> # export the private key to a file
            >>> key_pair.export_to_file('my_key_pair.pem', 'secret password')


        """
        with open(filename, 'w') as fp:
            fp.write(self.export_to_text(password))

    def __str__(self):
        return f'KeyPair {self.public_key}'

    @property
    def public_key_bytes(self):
        """

        Return the public key of the key pair in the byte format

        :returns: Address in bytes
        :rtype: byte

        .. code-block:: python

            >>> # create a keypair
            >>> key_pair = KeyPair()

            >>> # show the public key as bytes
            >>> print(key_pair.public_key_bytes)
            b'6\\xd8\\xc5\\xc4\\r\\xbe-\\x1b\\x011\\xac\\xf4\\x1c8..

        """
        public_key_bytes = self._public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return public_key_bytes

    @property
    def public_key(self):
        """

        Return the public key of the KeyPair in the format '0x....'

        :returns: public_key with leading '0x'
        :rtype: str

        .. code-block:: python

            >>> # create a random KeyPair
            >>> key_pair = KeyPair()

            >>> # show the public key as a hex string
            >>> print(key_pair.public_key)
            0x36d8c5c40dbe2d1b0131acf41c38b9d37ebe04d85...

        """
        return to_hex(self.public_key_bytes)

    @property
    def public_key_api(self):
        """

        Return the public key of the KeyPair without the leading '0x'

        :returns: public_key without the leading '0x'
        :rtype: str

        .. code-block:: python

            >>> # create a random KeyPair
            >>> key_pair = KeyPair()

            >>> # show the public key as a hex string with the leading '0x' removed
            >>> print(key_pair.public_key_api)
            36d8c5c40dbe2d1b0131acf41c38b9d37ebe04d85...


        """
        return remove_0x_prefix(self.public_key_checksum)

    @property
    def public_key_checksum(self):
        """

        Return the public key of the KeyPair with checksum upper/lower case characters

        :returns: str public_key in checksum format

        .. code-block:: python

            >>> # create a random KeyPair
            >>> key_pair = KeyPair()

            >>> # show the public key as a hex string in checksum format
            >>> print(key_pair.public_key_checksum)
            0x36D8c5C40dbE2D1b0131ACf41c38b9D37eBe04D85...

        """

        return to_public_key_checksum(self.public_key)

    def is_equal(self, public_key_pair: Union['KeyPair', str]):
        """

        Compare the value to see if it is the same as this key_pair

        :param: str, KeyPair public_key_pair: This can be a string ( public key) or a KeyPair object

        :returns: True if the public_key_pair str or KeyPair have the same public key as this object.

        """
        public_key = None
        if isinstance(public_key_pair, KeyPair):
            public_key = public_key_pair.public_key
        elif isinstance(public_key_pair, str):
            public_key = public_key_pair
        else:
            raise TypeError('invalid key_pair or public_key')

        return remove_0x_prefix(self.public_key_checksum).lower() == remove_0x_prefix(public_key).lower()

    @staticmethod
    def import_from_bytes(value: bytes) -> 'KeyPair':
        """

        Import an keypair from a private key in bytes.

        :returns: KeyPair object with the private/public key
        :rtype: KeyPair

        .. code-block:: python

            >>> # create an KeyPair object from a raw private key
            >>> key_pair = KeyPair.import_from_bytes(0x0x973f69bcd654b26475917072...)


        """
        return KeyPair(Ed25519PrivateKey.from_private_bytes(value))

    @staticmethod
    def import_from_text(text: Union[str, bytes], password: Union[str, bytes]) -> 'KeyPair':
        """

        Import a KeyPair from an encrypted PEM string.

        :param str text: PAM text string with the encrypted key text

        :param str password: password to decrypt the private key

        :returns: KeyPair object with the public/private key
        :rtype: KeyPair

        .. code-block:: python

            >>> # create an KeyPair object from a enrcypted pem text
            >>> pem_text = '''-----BEGIN ENCRYPTED PRIVATE KEY-----
                MIGbMFcGCSqGSIb3DQEFDTBKMCkGCSqGSIb3DQEFDDAcBAi3qm1zgjCO5gICCAAw
                DAYIKoZIhvcNAgkFADAdBglghkgBZQMEASoEENjvj1n...
            '''
            >>> key_pair = KeyPair.import_from_text(pem_text, 'my secret password')


        """
        if isinstance(password, str):
            password = password.encode()
        if isinstance(text, str):
            text = text.encode()

        private_key = serialization.load_pem_private_key(text, password, backend=default_backend())
        if private_key:
            return KeyPair(private_key)

    @staticmethod
    def import_from_mnemonic(words: str) -> 'KeyPair':
        """

        Creates a new KeyPair object using a list of words. These words contain the private key and must be kept secret.

        :param str words: List of mnemonic words to read

        :returns: KeyPair object with the public/private key
        :rtype: KeyPair

        .. code-block:: python

            >>> # create an KeyPair object from a mnemonic word list

            >>> key_pair = KeyPair.import_from_text('my word list that is the private key ..', 42)

        """

        mnemonic = Mnemonic('english')
        value = mnemonic.to_entropy(words)
        return KeyPair(Ed25519PrivateKey.from_private_bytes(value))

    @staticmethod
    def import_from_file(filename: str, password: Union[str, bytes]) -> 'KeyPair':
        """

        Load the encrypted private key from file. The file is saved in PEM format encrypted with a password

        :param str filename: Filename to read

        :param str password: password to decrypt the private key

        :returns: KeyPair with the private/public key
        :rtype: KeyPair

        .. code-block:: python

            >>> # create an KeyPair object from a enrcypted pem saved in a file
            >>> key_pair = KeyPair.import_from_file(my_key_pair_key.pem, 'my secret password')


        """
        with open(filename, 'r') as fp:
            return KeyPair.import_from_text(fp.read(), password)
