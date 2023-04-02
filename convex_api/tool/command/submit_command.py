"""

    Command Submit ..

"""
from argparse import Namespace
import json
from typing import Literal

from convex_api.tool.command.argparse_typing import BaseArgs, SubParsersAction
from convex_api.tool.output import Output

from .command_base import CommandBase

class SubmitArgs(BaseArgs):
    command: Literal['submit']
    submit: str
    name_address: str

class SubmitCommand(CommandBase):

    def __init__(self, sub_parser: SubParsersAction):
        self._command_list = []
        super().__init__('submit', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):

        parser = sub_parser.add_parser(
            self._name,
            description='call a convex query',
            help='Call a convex query command'

        )

        parser.add_argument(
            'submit',
            help='submit to perform'
        )

        parser.add_argument(
            'name_address',
            help='account address or account name, to use for the submit'
        )

        return parser

    def execute(self, args: Namespace, output: Output):
        submit_args = SubmitArgs.parse_obj(vars(args))

        convex = self.load_convex(submit_args.url)

        account = self.load_account(submit_args, submit_args.name_address, output)
        if not account:
            return

        result = convex.send(submit_args.submit, account)
        if not result:
            return
        
        output.add_line(json.dumps(result))
        output.set_values(result.dict())
