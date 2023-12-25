import aiosqlite
from fastapi import FastAPI, Depends, HTTPException
from result import Ok, Err, Result

import bank.database.accounts as accounts
import bank.database.utils as db_utils
from bank.database.database import rest_db
from bank.version import VERSION

app = FastAPI()


@app.get("/")
async def root():
    return {"version": VERSION}


@app.get("/account/info", response_model=db_utils.AccountInfo)
async def account_get(
    id: int | None = None,
    name: str | None = None,
    card_id: str | None = None,
    db: aiosqlite.Connection = Depends(rest_db),
) -> db_utils.AccountInfo:
    acc: accounts.Account | None = None
    acc_detail: str | None = None
    if id:
        acc = await accounts.get_account(db, id)
        acc_detail = f"id: {id}"
    elif name:
        acc = await accounts.get_account(db, name)
        acc_detail = f"name: {name}"
    elif card_id:
        acc = await accounts.get_account_from_card(db, card_id)
        acc_detail = f"card_id: {card_id}"

    if not acc:
        raise HTTPException(status_code=400, detail="No account identifier provided")

    r = await db_utils.get_account_info(db, acc.id)
    if isinstance(r, Ok):
        info = r.ok_value
        print(info.transactions)
        return info

    raise HTTPException(status_code=404, detail=f"Account {acc_detail} not found")


@app.post("/account/create")
async def account_create(
    acc: accounts.Account, db: aiosqlite.Connection = Depends(rest_db)
):
    """Create a new account"""
    account_id = await accounts.add_account(db, acc.name)
    if account_id:
        return accounts.Account(id=account_id, name=acc.name)

    raise HTTPException(status_code=409, detail=f"Failed to create account {acc.name}")
