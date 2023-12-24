from bank.models.schemas import Transaction
from bank.version import VERSION
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"version": VERSION}


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
