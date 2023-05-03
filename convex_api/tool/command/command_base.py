"""

    Command Base Class

"""

import logging
from abc import (
    ABC,
    abstractmethod
)
from argparse import (
    ArgumentParser,
    Namespace
)
from typing import (
    TypedDict,
    Union
)

from convex_api import (
    API,
    Account,
    KeyPair
)
from convex_api.tool.command.argparse_typing import (
    BaseArgs,
    SubParsersAction
)
from convex_api.tool.output import Output

logger = logging.getLogger('convex_tools')

DEFAULT_CONVEX_URL = 'https://convex.world'


class NameAddress(TypedDict):
    name: Union[str, None]
    address: int


class CommandBase(ABC):
    def __init__(self, name: str, sub_parser: Union[SubParsersAction, None] = None):
        self._name = name
        # TODO: If we include this it causes a type hinting error in resolve_to_name_address
        #       Should we somehow assert that load_convex has been called ?
        # self._convex = None
        self._sub_parser = sub_parser
        self._command_list: list['CommandBase'] = []
        if sub_parser:
            self.create_parser(sub_parser)

    def is_command(self, name: str) -> bool:
        return self._name == name

    def load_convex(self, url: Union[str, None], default_url: Union[str, None] = None) -> API:
        if url is None:
            url = default_url
        if url is None:
            url = DEFAULT_CONVEX_URL
        self._convex = API(url)
        return self._convex

    def process_sub_command(self, args: Namespace, output: Output, command: str):
        is_found = False
        for command_item in self._command_list:
            if command_item.is_command(command):
                command_item.execute(args, output)
                is_found = True
                break

        if not is_found:
            self.print_help()

    def print_help(self):
        if self._sub_parser is not None:
            self._sub_parser.choices[self._name].print_help()

    def resolve_to_name_address(self, name_address: Union[str, int], output: Output) -> Union[NameAddress, None]:
        name = None
        address = None

        if isinstance(name_address, str):
            address = self._convex.resolve_account_name(name_address)
            name = name_address

        if not address:
            address = Account.to_address(name_address)

        if not self.is_address(address):
            output.add_error(f'{address} is not an convex account address')
            return
        result: NameAddress = {
            'name': name,
            'address': address
        }
        return result

    def import_key_pair(self, args: BaseArgs):
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

    def load_account(self, args: BaseArgs, name_address: Union[str, int], output: Output):

        info = self.resolve_to_name_address(name_address, output)
        if not info:
            return

        key_pair = self.import_key_pair(args)
        if not key_pair:
            output.add_error('you need to set the "--keywords" or "--password" and "--keyfile/--keytext" to a valid account')
            return

        return Account(key_pair, info['address'], name=info['name'])

    def is_address(self, value: Union[int, str]) -> bool:
        return Account.is_address(value)

    @abstractmethod
    def create_parser(self, sub_parser: SubParsersAction) -> ArgumentParser:
        pass

    @abstractmethod
    def execute(self, args: Namespace, output: Output):
        pass

    @property
    def name(self) -> str:
        return self._name
