from asyncio import run as aiorun
from typing_extensions import Annotated

import typer
from result import Err, Ok, Result

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
