from bank.models.models import Transaction
from bank.models.rest import TransactionRest
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"version": "0.1.0"}


@app.get("/transactions")
async def tranasactions_get():
    return TransactionRest(
        transactions=[
            Transaction(sender="test", recipient="user", amount=10, notes=""),
        ]
    )
