from .models import Transaction
from pydantic import BaseModel


class TransactionRest(BaseModel):
    transactions: list[Transaction]
