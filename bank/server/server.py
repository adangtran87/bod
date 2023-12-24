import aiosqlite
from fastapi import FastAPI, Depends

import bank.database.accounts as accounts
from bank.database.database import rest_db
from bank.models.schemas import AccountList
from bank.version import VERSION

app = FastAPI()


@app.get("/")
async def root():
    return {"version": VERSION}


@app.get("/accounts/")
async def accounts_get(
    id: int | None = None,
    name: str | None = None,
    db: aiosqlite.Connection = Depends(rest_db),
) -> AccountList:
    output: AccountList = AccountList(accounts=[])
    if id:
        data = await accounts.get_account(db, id)
        if data:
            output = AccountList(accounts=[data])
    elif name:
        data = await accounts.get_account(db, name)
        if data:
            output = AccountList(accounts=[data])
    else:
        data = await accounts.get_accounts(db)
        output = AccountList(accounts=data)

    return output
