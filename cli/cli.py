import typer

from asyncio import run as aiorun

from bank.database.accounts import create_account_table

app = typer.Typer()


@app.command()
def test():
    print("Hello World")


@app.command()
def init_db():
    aiorun(create_account_table())


if __name__ == "__main__":
    app()
