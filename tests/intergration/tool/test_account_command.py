"""

    Test Account Command Tool

"""
from unittest.mock import Mock
from convex_api.account import Account

from convex_api.tool.command.account_balance_command import AccountBalanceCommand
from convex_api.tool.command.account_create_command import AccountCreateCommand
from convex_api.tool.command.account_info_command import AccountInfoCommand
from convex_api.tool.command.account_fund_command import AccountFundCommand
from convex_api.tool.command.account_name_resolve_command import AccountNameResolveCommand
from convex_api.tool.command.account_name_register_command import AccountNameRegisterCommand
from convex_api.tool.command.account_topup_command import AccountTopupCommand

from convex_api.tool.output import Output



def test_account_create_command(convex_url: str):
    args = Mock()

    args.url = convex_url
    args.password = 'test_password'
    args.keyfile = None
    args.keytext = None
    args.keywords = None
    args.name = None

    command = AccountCreateCommand()
    output = Output()
    command.execute(args, output)
    print(output.values)
    assert(output.values['keyfile'])
    assert(output.values['address'])
    assert(output.values['password'])



def test_account_balance_command(convex_url: str, test_account: Account):
    args = Mock()

    args.url = convex_url
    args.name_address = test_account.address

    command = AccountBalanceCommand()
    output = Output()
    command.execute(args, output)
    assert(output.values['balance'])


    args.url = convex_url
    args.name_address = test_account.name

    command = AccountBalanceCommand()
    output = Output()
    command.execute(args, output)
    assert(output.values['balance'])


def test_account_info_command(convex_url: str, test_account: Account):
    args = Mock()

    args.url = convex_url
    args.name_address = test_account.address

    command = AccountInfoCommand()
    output = Output()
    command.execute(args, output)
    assert(output.values['balance'])
    assert(output.values['address'])
    assert(output.values['sequence'])
    assert(output.values['type'])


    args.url = convex_url
    args.name_address = test_account.name

    command = AccountInfoCommand()
    output = Output()
    command.execute(args, output)
    assert(output.values['balance'])
    assert(output.values['address'])
    assert(output.values['sequence'])
    assert(output.values['type'])


def test_account_name_resolve_command(convex_url: str, test_account: Account):
    args = Mock()

    args.url = convex_url
    args.name = test_account.name

    command = AccountNameResolveCommand()
    output = Output()
    command.execute(args, output)
    assert(output.values['address'] == test_account.address)

def test_account_topup_command(convex_url: str, test_account: Account):
    args = Mock()

    args.url = convex_url
    args.keywords = test_account.key_pair.export_to_mnemonic
    args.keyfile = None
    args.keytext = None
    args.password = None
    args.name_address = test_account.address

    command = AccountTopupCommand()
    output = Output()
    command.execute(args, output)
    assert(output.values['balance'])

def test_account_fund_command(convex_url: str, test_account: Account):
    args = Mock()

    args.url = convex_url
    args.keywords = test_account.key_pair.export_to_mnemonic
    args.keyfile = None
    args.keytext = None
    args.password = None
    args.name_address = test_account.address
    args.amount = 1000

    command = AccountFundCommand()
    output = Output()
    command.execute(args, output)
    assert(output.values['balance'])
    assert(output.values['amount'] == args.amount) # type: ignore

def test_account_register_command(convex_url: str, test_account: Account):
    args = Mock()

    args.url = convex_url
    args.keywords = test_account.key_pair.export_to_mnemonic
    args.keyfile = None
    args.keytext = None
    args.password = None
    args.name_address = test_account.address
    args.name = test_account.name
    args.address = test_account.address

    command = AccountNameRegisterCommand()
    output = Output()
    command.execute(args, output)
    assert(output.values['name'] == args.name) # type: ignore
    assert(output.values['address'] == args.address) # type: ignore
