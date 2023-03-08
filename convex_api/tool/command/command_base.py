"""

    Command Base Class

"""

import logging

from abc import (
    ABC,
    abstractmethod
)

from convex_api import (
    API,
    Account,
    KeyPair
)
from convex_api.utils import is_address


logger = logging.getLogger('convex_tools')

DEFAULT_CONVEX_URL = 'https://convex.world'


class CommandBase(ABC):
    def __init__(self, name, sub_parser=None):
        self._name = name
        self._convex = None
        self._sub_parser = sub_parser
        if sub_parser:
            self.create_parser(sub_parser)

    def is_command(self, name):
        return self._name == name

    def load_convex(self, url, default_url=None):
        if url is None:
            url = default_url
        if url is None:
            url = DEFAULT_CONVEX_URL
        self._convex = API(url)
        return self._convex

    def process_sub_command(self, args, output, command):
        is_found = False
        for command_item in self._command_list:
            if command_item.is_command(command):
                command_item.execute(args, output)
                is_found = True
                break

        if not is_found:
            self.print_help()

    def print_help(self):
        self._sub_parser.choices[self._name].print_help()

    def resolve_to_name_address(self, name_address, output):
        name = None
        address = None
        if name_address:
            address = self._convex.resolve_account_name(name_address)
            name = name_address

        if not address:
            address = name_address

        if not self.is_address(address):
            output.add_error(f'{address} is not an convex account address')
            return
        return {
            'name': name,
            'address': address
        }

    def import_key_pair(self, args):
        key_pair = None
        if args.keyfile and args.password:
            logger.debug(f'importing keyfile {args.keyfile}')
            key_pair = KeyPair.import_from_file(args.keyfile, args.password)
        elif args.keywords:
            logger.debug('importing key from mnemonic')
            key_pair = KeyPair.import_from_mnemonic(args.keywords)
        elif args.keytext and args.password:
            logger.debug('importing keytext')
            key_pair = KeyPair.import_from_text(args.keytext, args.password)

        return key_pair

    def load_account(self, args, name_address, output):

        info = self.resolve_to_name_address(name_address, output)
        if not info:
            return

        key_pair = self.import_key_pair(args)
        if not key_pair:
            output.add_error('you need to set the "--keywords" or "--password" and "--keyfile/--keytext" to a valid account')
            return

        return Account(key_pair, info['address'], name=info['name'])

    def is_address(self, value):
        return Account.is_address(value)

    @abstractmethod
    def create_parser(self, sub_parser):
        pass

    @abstractmethod
    def execute(self, args, output):
        pass

    @property
    def name(self) -> str:
        return self._name
