"""

    Command Account Fund ..

"""

from argparse import Namespace
from typing import Literal, Union

from convex_api.tool.command.argparse_typing import (
    BaseArgs,
    SubParsersAction
)
from convex_api.tool.output import Output

from .command_base import CommandBase


class AccountFundArgs(BaseArgs):
    command: Literal['account']
    account_command: Literal['fund']
    amount: int
    name_address: str


class AccountFundCommand(CommandBase):

    def __init__(self, sub_parser: Union[SubParsersAction, None] = None):
        self._command_list = []
        super().__init__('fund', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):

        parser = sub_parser.add_parser(
            self._name,
            description='Request funds for an account',
            help='Request funds for an account'
        )

        parser.add_argument(
            'name_address',
            help='account address or account name'
        )

        parser.add_argument(
            'amount',
            type=int,
            help='amount to request funds for the account'
        )

        return parser

    def execute(self, args: Namespace, output: Output):
        typed_args = AccountFundArgs.parse_obj(vars(args))
        convex = self.load_convex(typed_args.url)

        account = self.load_account(typed_args, typed_args.name_address, output)
        if not account:
            return

        amount = convex.request_funds(typed_args.amount, account)
        balance = convex.get_balance(account)
        output.add_line(f'fund request for {amount} to balance: {balance} for account at {account.address}')
        output.set_value('amount', amount)
        output.set_value('balance', balance)
        output.set_value('address', account.address)
        if account.name:
            output.set_value('name', account.name)
