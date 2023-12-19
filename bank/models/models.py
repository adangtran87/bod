from pydantic import BaseModel


class Entity(BaseModel):
    name: str
    id: str


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: float
    notes: str
