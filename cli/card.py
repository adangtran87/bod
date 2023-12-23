from asyncio import run as aiorun
from typing_extensions import Annotated

import typer

from .utils import scan_card

app = typer.Typer()


@app.command()
def scan(
    device: Annotated[
        str, typer.Option(help="Device location string")
    ] = "tty:USB0:pn532",
):
    card_id = aiorun(scan_card(device))
    print(card_id)
