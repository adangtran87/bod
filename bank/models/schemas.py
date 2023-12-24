from pydantic import BaseModel

from bank.database.accounts import Account


class AccountList(BaseModel):
    """
    A list of accounts
    """

    accounts: list[Account]


class Transaction(BaseModel):
    """
    A singular transaction between two parties
    """

    sender: str
    recipient: str
    amount: float
    notes: str
