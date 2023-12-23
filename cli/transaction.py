from asyncio import run as aiorun
from pprint import pprint

import typer

import bank.database.database as database
import bank.database.transactions as transactions

app = typer.Typer()


@app.command()
def dump():
    """
    Dump all transactions
    """

    async def _get_cards() -> list[transactions.Transaction]:
        async with await database.get_db() as db:
            return await transactions.get_transactions(db)

    pprint(aiorun(_get_cards()))
