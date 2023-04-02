"""

    Command Account Topup ..

"""

from argparse import Namespace
from typing import Literal

from convex_api.tool.command.argparse_typing import (
    BaseArgs,
    SubParsersAction
)
from convex_api.tool.output import Output

from .command_base import CommandBase


class AccountTopupArgs(BaseArgs):
    command: Literal['account']
    account_command: Literal['topup']
    name_address: str


class AccountTopupCommand(CommandBase):

    def __init__(self, sub_parser: SubParsersAction):
        self._command_list = []
        super().__init__('topup', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):

        parser = sub_parser.add_parser(
            self._name,
            description='Topup an account with sufficient funds',
            help='Topup an account with sufficient funds'
        )

        parser.add_argument(
            'name_address',
            help='account address or account name'
        )

        return parser

    def execute(self, args: Namespace, output: Output):
        typed_args = AccountTopupArgs.parse_obj(vars(args))
        convex = self.load_convex(typed_args.url)
        account = self.load_account(typed_args, typed_args.name_address, output)
        if not account:
            return

        amount = convex.topup_account(account)
        balance = convex.get_balance(account)
        output.add_line(f'topup account by {amount} to balance: {balance} for account at {account.address}')
        output.set_value('amount', amount)
        output.set_value('balance', balance)
        output.set_value('address', account.address)
        if account.name:
            output.set_value('name', account.name)
