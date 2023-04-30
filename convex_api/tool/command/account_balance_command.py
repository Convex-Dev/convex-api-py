"""

    Command Account Balance ..

"""

from argparse import Namespace
from typing import (
    Literal,
    Union
)

from convex_api.tool.command.argparse_typing import (
    BaseArgs,
    SubParsersAction
)
from convex_api.tool.output import Output

from .command_base import CommandBase

DEFAULT_AMOUNT = 10


class AccountBalanceArgs(BaseArgs):
    command: Literal['account']
    account_command: Literal['balance']
    name_address: Union[str, int]


class AccountBalanceCommand(CommandBase):

    def __init__(self, sub_parser: Union[SubParsersAction, None] = None):
        super().__init__('balance', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):

        parser = sub_parser.add_parser(
            self._name,
            description='Get balance from an account address or name',
            help='Get balance of an account'

        )

        parser.add_argument(
            'name_address',
            help='account address or account name'
        )

        return parser

    def execute(self, args: Namespace, output: Output):
        typed_args = AccountBalanceArgs.parse_obj(vars(args))
        convex = self.load_convex(typed_args.url)
        info = self.resolve_to_name_address(typed_args.name_address, output)
        if not info:
            return

        balance = convex.get_balance(info['address'])
        output.add_line(f'balance: {balance} for account at {info["address"]}')
        output.set_value('balance', balance)
        output.set_value('address', info['address'])
        if info['name']:
            output.set_value('name', info['name'])
