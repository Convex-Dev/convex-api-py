"""

    Account Commands

"""

from argparse import Namespace
from typing import (
    Literal,
    cast
)

from convex_api.tool.command.argparse_typing import (
    BaseArgs,
    SubParsersAction
)
from convex_api.tool.output import Output

from .account_balance_command import AccountBalanceCommand
from .account_create_command import AccountCreateCommand
from .account_fund_command import AccountFundCommand
from .account_info_command import AccountInfoCommand
from .account_name_register_command import AccountNameRegisterCommand
from .account_name_resolve_command import AccountNameResolveCommand
from .account_topup_command import AccountTopupCommand
from .command_base import CommandBase
from .help_command import HelpCommand


class AccountArgs(BaseArgs):
    command: Literal['account']
    account_command: Literal['balance', 'create', 'info', 'fund', 'name', 'resolve', 'topup', 'help']


class AccountCommand(CommandBase):

    def __init__(self, sub_parser: SubParsersAction):
        self._command_list = []
        super().__init__('account', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):
        parser = sub_parser.add_parser(
            self._name,
            description='Tool tasks on accounts',
            help='Tasks to perform on accounts',

        )
        account_parser = cast(SubParsersAction, parser.add_subparsers(
            title='Account sub command',
            description='Account sub command',
            help='Account sub command',
            dest='account_command'
        ))

        self._command_list = [
            AccountBalanceCommand(account_parser),
            AccountCreateCommand(account_parser),
            AccountInfoCommand(account_parser),
            AccountFundCommand(account_parser),
            AccountNameRegisterCommand(account_parser),
            AccountNameResolveCommand(account_parser),
            AccountTopupCommand(account_parser),
            HelpCommand(account_parser, self)
        ]
        return parser

    def execute(self, args: Namespace, output: Output):
        return self.process_sub_command(args, output, args.account_command)
