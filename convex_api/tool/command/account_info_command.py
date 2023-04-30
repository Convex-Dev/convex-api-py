"""

    Command Account Info ..

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


class AccountInfoArgs(BaseArgs):
    command: Literal['account']
    account_command: Literal['info']
    name_address: Union[str, int]


class AccountInfoCommand(CommandBase):

    def __init__(self, sub_parser: Union[SubParsersAction, None] = None):
        self._command_list = []
        super().__init__('info', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):

        parser = sub_parser.add_parser(
            self._name,
            description='Get account information',
            help='Get account information'

        )

        parser.add_argument(
            'name_address',
            help='account address or account name'
        )

        return parser

    def execute(self, args: Namespace, output: Output):
        typed_args = AccountInfoArgs.parse_obj(vars(args))
        convex = self.load_convex(typed_args.url)
        info = self.resolve_to_name_address(typed_args.name_address, output)
        if not info:
            return

        account_info = convex.get_account_info(info['address'])
        output.set_value('address', info['address'])
        if info['name']:
            output.set_value('name', info['name'])
        output.add_line_values(account_info.dict())
        output.set_values(account_info.dict())
