"""

    Command Query ..

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


class QueryArgs(BaseArgs):
    command: Literal['query']
    query: str
    name_address: Union[str, int]


class QueryCommand(CommandBase):

    def __init__(self, sub_parser: Union[SubParsersAction, None] = None):
        self._command_list = []
        super().__init__('query', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):

        parser = sub_parser.add_parser(
            self._name,
            description='call a convex query',
            help='Call a convex query command'

        )

        parser.add_argument(
            'query',
            help='query to perform'
        )

        parser.add_argument(
            'name_address',
            nargs='?',
            help='account address or account name. Defaults: Address #1'
        )

        return parser

    def execute(self, args: Namespace, output: Output):
        query_args = QueryArgs.parse_obj(vars(args))

        convex = self.load_convex(query_args.url)

        if query_args.name_address:
            info = self.resolve_to_name_address(query_args.name_address, output)
            if not info:
                return
            address = info['address']

        address = 1
        result = convex.query(query_args.query, address)
        output.add_line(result.json())
        output.set_values(result.dict())
