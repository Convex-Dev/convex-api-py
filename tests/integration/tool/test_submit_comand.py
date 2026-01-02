"""

    Test Submit

"""
from unittest.mock import Mock
from convex_api.account import Account

from convex_api.tool.command.submit_command import SubmitCommand
from convex_api.tool.output import Output


def test_submit_command(convex_url: str, test_account: Account):
    args = Mock()

    args.command = 'submit'
    args.url = convex_url
    args.keywords = test_account.key_pair.export_to_mnemonic
    args.keyfile = None
    args.keytext = None
    args.password = None

    args.submit = '(map inc [1 2 3 4 5])'
    args.name_address = test_account.address

    command = SubmitCommand()
    output = Output()
    command.execute(args, output)
    assert output.values['value'] == [2, 3, 4, 5, 6]
