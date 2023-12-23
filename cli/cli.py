from typing_extensions import Annotated
import typer

from asyncio import run as aiorun

import bank.database.accounts as accounts
import bank.database.cards as cards
import bank.database.database as database
import bank.app.nfcutils.nfcutils as nfc

app = typer.Typer()


@app.command()
def test():
    print("Hello World")


@app.command()
def init_db():
    async def _init_db():
        async with await database.get_db() as db:
            await accounts.create_table(db)
            await cards.create_table(db)

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


async def _scan_card(device: str) -> str:
    dev = nfc.NfcDevice(device)
    print("Tap Card:")
    await dev.connect()
    if dev.has_data():
        data = await dev.get_data()
        print(data)
        return ""
    else:
        return ""


@app.command()
def scan_card(
    device: Annotated[
        str, typer.Option(help="Device location string")
    ] = "tty:USB0:pn532",
):
    card_id = aiorun(_scan_card(device))
    print(card_id)


if __name__ == "__main__":
    app()
