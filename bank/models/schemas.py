from pydantic import BaseModel


class Transaction(BaseModel):
    """
    A singular transaction between two parties
    """

    sender: str
    recipient: str
    amount: float
    notes: str
