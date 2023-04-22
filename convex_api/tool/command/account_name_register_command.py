"""

    Command Account Register ..

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


class AccountNameRegisterArgs(BaseArgs):
    command: Literal['account']
    account_command: Literal['register']
    name_address: str
    name: str
    address: str


class AccountNameRegisterCommand(CommandBase):

    def __init__(self, sub_parser: Union[SubParsersAction, None] = None):
        self._command_list = []
        super().__init__('register', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):

        parser = sub_parser.add_parser(
            self._name,
            description='Register an account name',
            help='Register an account name'
        )

        parser.add_argument(
            'name_address',
            help='account address or account name to pay and the owner of the registration'
        )

        parser.add_argument(
            'name',
            help='account account name to register'
        )

        parser.add_argument(
            'address',
            help='account address to register'
        )

        return parser

    def execute(self, args: Namespace, output: Output):
        typed_args = AccountNameRegisterArgs.parse_obj(vars(args))
        convex = self.load_convex(typed_args.url)

        account = self.load_account(typed_args, typed_args.name_address, output)
        if not account:
            return

        if not self.is_address(typed_args.address):
            output.add_error(f'{typed_args.address} to register is not an convex account address')
            return

        register_account = convex.register_account_name(typed_args.name, typed_args.address, account)
        if not register_account:
            output.add_error('failet to register acccount')
            return

        output.add_line(f'registered account name {register_account.name} to address {register_account.address}')
        output.set_value('address', register_account.address)
        if register_account.name:
            output.set_value('name', register_account.name)
