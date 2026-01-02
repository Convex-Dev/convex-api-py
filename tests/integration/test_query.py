"""
Test read-only queries on Convex network.

These tests connect to a remote Convex instance and run queries.
Queries are read-only operations that do not require key pairs or authentication.
"""

import pytest

from convex_api.account import Account
from tests.common import get_convex


def test_query_balance_standard_account(convex_url: str):
    """Test querying balance of a standard account address."""
    convex = get_convex(convex_url)
    
    # Query balance of account #1 (standard account)
    result = convex.query('(balance #1)', 1)
    assert result is not None
    assert 'value' in result.model_dump()
    # Balance should be a non-negative integer
    assert isinstance(result.value, int)
    assert result.value >= 0


def test_query_address_function(convex_url: str):
    """Test querying address of a function/contract."""
    convex = get_convex(convex_url)
    
    # Query address of the registry
    result = convex.query('(address *registry*)', 1)
    assert result is not None
    assert 'value' in result.model_dump()
    # Should return an address (can be None if not found, or an address)
    assert result.value is None or isinstance(result.value, (int, str))


def test_query_simple_arithmetic(convex_url: str):
    """Test simple arithmetic queries."""
    convex = get_convex(convex_url)
    
    # Simple addition
    result = convex.query('(+ 1 2 3)', 1)
    assert result is not None
    assert result.value == 6
    
    # Simple multiplication
    result = convex.query('(* 2 3 4)', 1)
    assert result is not None
    assert result.value == 24
    
    # Simple subtraction
    result = convex.query('(- 10 3)', 1)
    assert result is not None
    assert result.value == 7


def test_query_list_operations(convex_url: str):
    """Test list operations in queries."""
    convex = get_convex(convex_url)
    
    # Map operation
    result = convex.query('(map inc [1 2 3 4 5])', 1)
    assert result is not None
    assert result.value == [2, 3, 4, 5, 6]
    
    # Count operation
    result = convex.query('(count [1 2 3 4 5])', 1)
    assert result is not None
    assert result.value == 5
    
    # First operation
    result = convex.query('(first [10 20 30])', 1)
    assert result is not None
    assert result.value == 10


def test_query_balance_multiple_accounts(convex_url: str):
    """Test querying balances of multiple standard accounts."""
    convex = get_convex(convex_url)
    
    # Query balances of several standard accounts
    for account_num in [1, 2, 3]:
        result = convex.query(f'(balance #{account_num})', account_num)
        assert result is not None
        assert 'value' in result.model_dump()
        assert isinstance(result.value, int)
        assert result.value >= 0


def test_query_address_checksum(convex_url: str):
    """Test querying address checksum conversion."""
    convex = get_convex(convex_url)
    
    # Query address of account #1 as checksum
    result = convex.query('(address #1)', 1)
    assert result is not None
    assert 'value' in result.model_dump()
    # Should return a checksum address (string) or the address itself
    address = Account.to_address(result.value)
    assert address == 1


def test_query_conditional_logic(convex_url: str):
    """Test conditional logic in queries."""
    convex = get_convex(convex_url)
    
    # If statement
    result = convex.query('(if true 42 0)', 1)
    assert result is not None
    assert result.value == 42
    
    result = convex.query('(if false 42 0)', 1)
    assert result is not None
    assert result.value == 0
    
    # Comparison
    result = convex.query('(> 10 5)', 1)
    assert result is not None
    assert result.value is True
    
    result = convex.query('(< 10 5)', 1)
    assert result is not None
    assert result.value is False


def test_query_string_operations(convex_url: str):
    """Test string operations in queries."""
    convex = get_convex(convex_url)
    
    # String concatenation
    result = convex.query('(str "Hello" " " "World")', 1)
    assert result is not None
    assert result.value == "Hello World"
    
    # String length (if available)
    # Note: This depends on available Convex functions


def test_query_nested_expressions(convex_url: str):
    """Test nested expressions in queries."""
    convex = get_convex(convex_url)
    
    # Nested arithmetic
    result = convex.query('(+ (* 2 3) (- 10 4))', 1)
    assert result is not None
    assert result.value == 12  # (2*3) + (10-4) = 6 + 6 = 12
    
    # Nested list operations
    result = convex.query('(map (fn [x] (* x 2)) [1 2 3])', 1)
    assert result is not None
    assert result.value == [2, 4, 6]


def test_query_with_different_addresses(convex_url: str):
    """Test that queries work with different account addresses."""
    convex = get_convex(convex_url)
    
    # Same query with different account addresses should work
    query = '(+ 1 1)'
    
    for address in [1, 2, 3]:
        result = convex.query(query, address)
        assert result is not None
        assert result.value == 2


def test_query_resolve_name(convex_url: str):
    """Test querying name resolution."""
    convex = get_convex(convex_url)
    
    # Try to resolve a known name (if available)
    # This tests the resolve_name functionality via query
    # Note: The name may not exist, which is expected behavior
    from convex_api.exceptions import ConvexAPIError
    
    result = convex.query('(address @convex.trust)', 1)
    assert result is not None
    # If the name exists, it should return an address
    if result.value is not None:
        address = Account.to_address(result.value)
        assert isinstance(address, int)
        assert address > 0

