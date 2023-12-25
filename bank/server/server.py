import aiosqlite
from fastapi import FastAPI, Depends, HTTPException
from result import Ok, Err, Result

import bank.database.accounts as accounts
import bank.database.utils as db_utils
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
    """Get account resources"""
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


@app.get("/account/info/{account_id}", response_model=db_utils.AccountInfo)
async def account_get(
    account_id: int, db: aiosqlite.Connection = Depends(rest_db)
) -> db_utils.AccountInfo:
    r = await db_utils.get_account_info(db, account_id)
    if isinstance(r, Ok):
        return r.ok_value

    raise HTTPException(status_code=404, detail=f"Account {account_id} not found")


@app.post("/account/create")
async def account_create(
    acc: accounts.Account, db: aiosqlite.Connection = Depends(rest_db)
):
    """Create a new account"""
    account_id = await accounts.add_account(db, acc.name)
    if account_id:
        return accounts.Account(id=account_id, name=acc.name)

    raise HTTPException(status_code=409, detail=f"Failed to create account {acc.name}")
