from typing import Any

from pydantic import (
    BaseModel,
    Field
)


class ErrorResponse(BaseModel):
    """REST API error response."""
    errorCode: int
    value: Any


class CreateAccountRequest(BaseModel):
    """REST API request for a create account request."""
    accountKey: str | None = Field(None, min_length=64, max_length=64)


class CreateAccountResponse(BaseModel):
    """REST API response from a create account request."""
    address: int


class AccountDetailsResponse(BaseModel):
    """REST API response from an account details request."""
    sequence: int
    address: int
    memorySize: int
    balance: int
    allowance: int
    type: str


class FaucetRequest(BaseModel):
    """REST API request for a faucet request."""
    address: int
    amount: int


class FaucetResponse(BaseModel):
    """REST API response from a faucet request."""
    address: int
    amount: int
    value: int | None = None


class QueryRequest(BaseModel):
    """REST API request for a query request."""
    address: int
    source: str


class QueryResponse(BaseModel):
    """REST API response from a query request."""
    value: Any
    errorCode: str | None = None


class PrepareTransactionRequest(BaseModel):
    """REST API request for a prepare transaction request."""
    address: int
    source: str
    sequence: int | None = None


class PrepareTransactionResponse(BaseModel):
    """REST API response from a prepare transaction request."""
    address: int
    hash: str | None = None
    sequence: int
    source: str


class SubmitTransactionRequest(BaseModel):
    """REST API request for a submit transaction request."""
    address: int
    accountKey: str | None = Field(None, min_length=64, max_length=64)
    hash: str | None = None
    sig: str | None = Field(None, min_length=128, max_length=128)


class SubmitTransactionResponse(BaseModel):
    """REST API response from a submit transaction request."""
    value: Any
    errorCode: str | None = None
