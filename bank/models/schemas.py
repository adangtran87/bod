from pydantic import BaseModel
from pydantic.types import UUID4


class Account(BaseModel):
    """
    An account participates in transactions
    """

    name: str
    id: UUID4
    card_ids: list[str]


class Transaction(BaseModel):
    """
    A singular transaction between two parties
    """

    sender: Account
    recipient: Account
    amount: float
    notes: str
