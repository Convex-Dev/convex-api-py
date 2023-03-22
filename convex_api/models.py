from pydantic import BaseModel, Field
from typing import Any


class CreateAccountRequest(BaseModel):
    """Request for a create account request."""
    accountKey: str = Field(None, min_length=64, max_length=64)


class CreateAccountResponse(BaseModel):
    """Response from a create account request."""
    address: int


class AccountDetailsResponse(BaseModel):
    """Response from an account details request."""
    sequence: int
    address: int
    memorySize: int
    balance: int
    allowance: int
    type: str


class FaucetRequest(BaseModel):
    """Request for a faucet request."""
    address: int
    amount: int


class FaucetResponse(BaseModel):
    """Response from a faucet request."""
    address: int
    amount: int
    value: int


class QueryRequest(BaseModel):
    """Request for a query request."""
    address: int
    source: str


class QueryResponse(BaseModel):
    """Response from a query request."""
    value: Any


class PrepareTransactionRequest(BaseModel):
    """Request for a prepare transaction request."""
    address: int
    source: str
 

class PrepareTransactionResponse(BaseModel):
    """Response from a prepare transaction request."""
    address: int
    hash: str = Field(None, min_length=64, max_length=64)
    sequence: int
    source: str


class SubmitTransactionRequest(BaseModel):
    """Request for a submit transaction request."""
    address: int
    accountKey: str = Field(None, min_length=64, max_length=64)
    hash: str = Field(None, min_length=64, max_length=64)
    sig: str = Field(None, min_length=128, max_length=128)


class SubmitTransactionResponse(BaseModel):
    """Response from a submit transaction request."""
    value: Any

