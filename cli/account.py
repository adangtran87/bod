from asyncio import run as aiorun
from pprint import pprint

import typer

import bank.database.accounts as accounts
import bank.database.database as database

app = typer.Typer()


@app.command()
def add(name: str):
    async def _add_account(name: str):
        async with await database.get_db() as db:
            await accounts.add_account(db, name)

    aiorun(_add_account(name))


@app.command()
def dump():
    async def _get_accounts() -> list[accounts.Account]:
        async with await database.get_db() as db:
            return await accounts.get_accounts(db)

    pprint(aiorun(_get_accounts()))
