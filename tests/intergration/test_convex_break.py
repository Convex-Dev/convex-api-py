"""


    Test Convex Breaking

"""

import pytest
import secrets

from convex_api.account import Account
from convex_api.api import API
from convex_api.exceptions import ConvexAPIError


def test_convex_recursion(convex: API, test_account: Account):
    chain_length = 4
    address_list: list[int] = []
    for index in range(0, chain_length):
        contract = f"""
(def chain-{index}
    (deploy
        '(do
            (def stored-data
                ^{{:private? true}}
                nil
            )
            (def chain-address
                ^{{:private? true}}
                nil
            )
            (defn get
                ^{{:callable? true}}
                []
                (call chain-address (get))
            )
            (defn set
                ^{{:callable? true}}
                [x]
                ( if chain-address (call chain-address(set x)) (def stored-data x))
            )
            (defn set-chain-address
                ^{{:callable? true}}
                [x]
                (def chain-address x)
            )
        )
    )
)
"""
        convex.topup_account(test_account)
        result = convex.send(contract, test_account)
        assert(result is not None)
        address_list.append(Account.to_address(result.value))
    for index in range(0, chain_length):
        next_index = index + 1
        if next_index == chain_length:
            next_index = 0
        call_address = address_list[next_index]
        result = convex.send(f'(call chain-{index} (set-chain-address #{call_address}))', test_account)
        test_number = secrets.randbelow(1000)
        if index == chain_length - 1:
            with pytest.raises(ConvexAPIError, match='DEPTH'):
                result = convex.send(f'(call chain-{index} (set {test_number}))', test_account)
        else:
            result = convex.send(f'(call chain-0 (set {test_number}))', test_account)
            assert(result is not None)
            assert(result.value == test_number)
    with pytest.raises(ConvexAPIError, match='DEPTH'):
        convex.query('(call chain-0 (get))', test_account)

def test_schedule_transfer(convex: API, test_account: Account, other_account: Account):
    # you can send coins to an actor , if it exports the receive-coin function

    contract = """
(def transfer-for-ever
    (deploy
        '(do
            (defn tx-delay
                ^{:callable? true}
                [to-address amount]
                (transfer to-address amount)
                (def call-address *address*)
                (schedule (+ *timestamp* 1000) (call call-address (tx-delay to-address amount)))
            )
            (defn tx-now
                ^{:callable? true}
                [to-address amount]
                (transfer to-address amount)
            )
            (defn show-schedule
                ^{:callable? true}
                []
                [(get *state* :schedule) *address*]
            )
            (defn receive-coin
                ^{:callable? true}
                [sender amount data]
                (accept amount)
            )
        )
    )
)
"""
# (call contract-address (tx-to to-address amount))

    convex.topup_account(test_account)
    convex.topup_account(other_account, 8000000)
    result = convex.send(contract, test_account)
    assert(result is not None)
    contract_address = Account.to_address(result.value)
    convex.transfer(contract_address, 800000, other_account)
    convex.topup_account(test_account)
    result = convex.send(f'(call #{contract_address} (tx-delay #{other_account.address} 1000))', test_account)
    print(result)
    result = convex.send(f'(call #{contract_address} (show-schedule))', test_account)
    print(result)
