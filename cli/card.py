from asyncio import run as aiorun
from pprint import pprint
from typing_extensions import Annotated

import typer
from result import Ok

import bank.database.cards as cards
import bank.database.database as database
from .utils import scan_card

app = typer.Typer()


@app.command()
def scan(
    device: Annotated[
        str, typer.Option(help="Device location string")
    ] = "tty:USB0:pn532",
):
    r = aiorun(scan_card(device))
    if isinstance(r, Ok):
        print(f"Card Id: {r.ok_value}")
    else:
        print(f"ERROR: {r.err_value}")


@app.command()
def dump():
    async def _get_cards() -> list[cards.Card]:
        async with await database.get_db() as db:
            return await cards.get_cards(db)

    pprint(aiorun(_get_cards()))
