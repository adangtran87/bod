from asyncio import run as aiorun

import typer

import bank.database.accounts as accounts
import bank.database.cards as cards
import bank.database.database as database

app = typer.Typer()


@app.command()
def init():
    async def _init_db():
        async with await database.get_db() as db:
            await accounts.create_table(db)
            await cards.create_table(db)

    aiorun(_init_db())


@app.command()
def seed():
    async def _test_db():
        async with await database.get_db() as db:
            for i in range(1, 4):
                await accounts.add_account(db, f"test{i}")

    init()
    aiorun(_test_db())
