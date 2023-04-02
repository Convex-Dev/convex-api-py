"""

    Command Account Name Resolve ..

"""

from argparse import Namespace
from typing import Literal

from convex_api.tool.command.argparse_typing import (
    BaseArgs,
    SubParsersAction
)
from convex_api.tool.output import Output

from .command_base import CommandBase


class AccountNameResolveArgs(BaseArgs):
    command: Literal['account']
    account_command: Literal['resolve']
    name: str


class AccountNameResolveCommand(CommandBase):

    def __init__(self, sub_parser: SubParsersAction):
        super().__init__('resolve', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):

        parser = sub_parser.add_parser(
            self._name,
            description='Get an address from an account name',
            help='Get an address from an account name'

        )

        parser.add_argument(
            'name',
            help='account name to resolve'
        )

        return parser

    def execute(self, args: Namespace, output: Output):
        typed_args = AccountNameResolveArgs.parse_obj(vars(args))
        convex = self.load_convex(typed_args.url)
        address = convex.resolve_account_name(typed_args.name)
        if address:
            output.add_line(f'address: {address}')
            output.set_value('address', address)
        else:
            output.add_line('not found')

        output.set_value('name', typed_args.name)
