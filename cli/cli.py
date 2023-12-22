import typer

from asyncio import run as aiorun

import bank.database.accounts as accounts

app = typer.Typer()


@app.command()
def test():
    print("Hello World")


@app.command()
def init_db():
    aiorun(accounts.create_table())


@app.command()
def add_account(name: str):
    aiorun(accounts.add_account(name))


@app.command()
def get_accounts():
    print(aiorun(accounts.get_accounts()))


if __name__ == "__main__":
    app()
