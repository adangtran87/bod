import uuid

from bank.models.schemas import Account, Transaction
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"version": "0.1.0"}


@app.get("/transactions")
async def tranasactions_get():
    return [
        Transaction(
            sender=Account(name="bank", id=uuid.uuid4(), card_ids=[]),
            recipient=Account(name="user", id=uuid.uuid4(), card_ids=[]),
            amount=10,
            notes="",
        ),
    ]
