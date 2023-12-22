from bank.models.schemas import Transaction
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"version": "0.1.0"}


@app.get("/transactions")
async def tranasactions_get():
    return [
        Transaction(
            sender="bank",
            recipient="user",
            amount=10,
            notes="",
        ),
    ]
