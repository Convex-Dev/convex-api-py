"""


    Test Convex Breaking

"""

import pytest
import secrets

from tests.helpers import auto_topup_account

from convex_api.account import Account
from convex_api.convex_api import ConvexAPI
from convex_api.exceptions import ConvexAPIError


def test_convex_recursion(convex, test_account):
    chain_length = 4
    address_list = []
    for index in range(0, chain_length):
        contract = f"""
(def chain-{index}
    (deploy
        '(do
            (def stored-data nil)
            (def chain-address nil)
            (defn get [] (call chain-address (get)))
            (defn set [x] (if chain-address (call chain-address(set x)) (def stored-data x)) )
            (defn set-chain-address [x] (def chain-address x))
            (export get set set-chain-address)
        )
    )
)
"""
        auto_topup_account(convex, test_account)
        result = convex.send(contract, test_account)
        address_list.append(result['value'])
    for index in range(0, chain_length):
        next_index = index + 1
        if next_index == chain_length:
            next_index = 0
        call_address = address_list[next_index]
        result = convex.send(f'(call chain-{index} (set-chain-address {call_address}))', test_account)
        test_number = secrets.randbelow(1000)
        if index == chain_length - 1:
            with pytest.raises(ConvexAPIError, match='DEPTH'):
                result = convex.send(f'(call chain-{index} (set {test_number}))', test_account)
        else:
            result = convex.send(f'(call chain-0 (set {test_number}))', test_account)
            assert(result)
            assert(result['value'] == test_number)
    with pytest.raises(ConvexAPIError, match='DEPTH'):
        convex.query('(call chain-0 (get))', test_account)

def test_schedule_transfer(convex, test_account, other_account):
    contract = """
(def transfer-for-ever
    (deploy
        '(do
            (def call-counter 0)
            (defn tx-delay [to-address amount event-time]
                (schedule event-time (tx-now to-address amount))
            )
            (defn tx-now [to-address amount]
                (def call-counter (+ call-counter 1))
                (schedule (+ *timestamp* 1000) (tx-now to-address amount))
                (transfer to-address amount)
            )
            (defn counter [] call-counter)
            (export tx-delay tx-now counter)
        )
    )
)
"""
# (call contract-address (tx-to to-address amount))

    auto_topup_account(convex, test_account)
    result = convex.send(contract, test_account)
    contract_address = result['value']
    convex.transfer(contract_address, 8000000, other_account)
    auto_topup_account(convex, test_account)
    result = convex.send(f'(call transfer-for-ever (tx-now {other_account.address} 1000))', test_account)
    print(result)

    #for index in range(0, 10):
        #result = convex.query('(call transfer-for-ever (counter))', test_account)
        #print(result)
