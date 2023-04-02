"""

    Command peer

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

from .command_base import CommandBase
from .help_command import HelpCommand
from .peer_create_command import PeerCreateCommand


class PeerArgs(BaseArgs):
    command: Literal['peer']
    peer_command: Literal['create', 'help']


class PeerCommand(CommandBase):

    def __init__(self, sub_parser: SubParsersAction):
        super().__init__('peer', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):
        parser = sub_parser.add_parser(
            self._name,
            description='Tool tasks on peers',
            help='Tasks to perform on peers',

        )
        peer_parser = cast(SubParsersAction, parser.add_subparsers(
            title='Peer sub command',
            description='Peer sub command',
            help='Peer sub command',
            dest='peer_command'
        ))

        self._command_list = [
            PeerCreateCommand(peer_parser),
            HelpCommand(peer_parser, self)
        ]
        return parser

    def execute(self, args: Namespace, output: Output):
        return self.process_sub_command(args, output, args.peer_command)
