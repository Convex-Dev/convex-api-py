"""

    Test Convex api

"""
import secrets

from convex_api.convex_api import ConvexAPI


def test_convex_api_request_funds(test_account, convex_url):
    convex = ConvexAPI(convex_url)
    amount = secrets.randbelow(100) + 1
    request_amount = convex.request_funds(test_account, amount)
    assert(request_amount == amount)

def test_convex_api_send_transaction(test_account, convex_url):
    convex = ConvexAPI(convex_url)
    request_amount = convex.request_funds(test_account, 10000000)
    result = convex.send_transaction(test_account, '(map inc [1 2 3 4 5])')
    assert(result == [2, 3, 4, 5, 6])
