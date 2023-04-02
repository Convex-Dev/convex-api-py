"""

    Command Help
"""

from typing import Any
from convex_api.tool.command.argparse_typing import SubParsersAction
from convex_api.tool.output import Output
from .command_base import CommandBase


class HelpCommand(CommandBase):

    def __init__(self, sub_parser: SubParsersAction, parent_command: CommandBase):
        self._parent_command = parent_command
        super().__init__('help', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):

        parser = sub_parser.add_parser(
            self._name,
            description='Get help about this command section',
            help='Get more help'

        )
        return parser

    def execute(self, args: Any, output: Output):
        self._parent_command.print_help()
