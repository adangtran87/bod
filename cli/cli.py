import typer

from asyncio import run as aiorun

import bank.database.accounts as accounts
import bank.database.database as database

app = typer.Typer()


@app.command()
def test():
    print("Hello World")


@app.command()
def init_db():
    async def _init_db():
        async with await database.get_db() as db:
            await accounts.create_table(db)

    aiorun(_init_db())


@app.command()
def test_db():
    async def _test_db():
        async with await database.get_db() as db:
            for i in range(1, 4):
                await accounts.add_account(db, f"test{i}")

    init_db()
    aiorun(_test_db())


@app.command()
def add_account(name: str):
    async def _add_account(name: str):
        async with await database.get_db() as db:
            await accounts.add_account(db, name)

    aiorun(_add_account(name))


@app.command()
def get_accounts():
    async def _get_accounts() -> list[accounts.Account]:
        async with await database.get_db() as db:
            return await accounts.get_accounts(db)

    print(aiorun(_get_accounts()))

if __name__ == "__main__":
    app()
