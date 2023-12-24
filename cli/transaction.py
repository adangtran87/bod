from asyncio import run as aiorun
from datetime import datetime
from pprint import pprint
from typing_extensions import Annotated
from typing import Optional

import typer
from result import Err, Ok, Result

import bank.database.database as database
import bank.database.transactions as transactions

from cli.utils import scan_card

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


@app.command()
def add(
    value: Annotated[float, typer.Argument(help="Transaction value")],
    device: Annotated[
        str, typer.Option(help="Device location string")
    ] = "tty:USB0:pn532",
    note: Annotated[Optional[str], typer.Option(help="Transaction note")] = None,
):
    """Add a transaction "to a card"

    This assumes the user has run "cli account add --scan" prior
    to create an account associated with a card
    """

    async def _scan_and_add(
        value: float, device: str, note: str | None
    ) -> Result[str, str]:
        r = await scan_card(device)
        if isinstance(r, Ok):
            card_id = r.ok_value
            t = transactions.Transaction(
                id=0, date=datetime.now(), value=value, account_id=0, note=note
            )
            async with await database.get_db() as db:
                t_id = await transactions.add_transaction_from_card_id(
                    db, card_id=card_id, t=t
                )
                result = {
                    "id": t_id,
                    "value": value,
                    "note": note,
                }
                if t_id:
                    return Ok(f"Created transaction {result}")
                else:
                    return Err(f"No account registered to card: {card_id}")
        else:
            return Err(r.err_value)

    r = aiorun(_scan_and_add(value, device, note))
    if isinstance(r, Ok):
        pprint(r.ok_value)
    else:
        pprint(r.err_value)


@app.command()
def sub(
    value: Annotated[float, typer.Argument(help="Value to subtract")],
    device: Annotated[
        str, typer.Option(help="Device location string")
    ] = "tty:USB0:pn532",
    note: Annotated[Optional[str], typer.Option(help="Transaction note")] = None,
):
    """Add a transaction "to a card"

    This assumes the user has run "cli account add --scan" prior
    to create an account associated with a card
    """

    async def _scan_and_add(
        value: float, device: str, note: str | None
    ) -> Result[str, str]:
        r = await scan_card(device)
        if isinstance(r, Ok):
            card_id = r.ok_value
            t = transactions.Transaction(
                id=0, date=datetime.now(), value=-value, account_id=0, note=note
            )
            async with await database.get_db() as db:
                t_id = await transactions.add_transaction_from_card_id(
                    db, card_id=card_id, t=t
                )
                result = {
                    "id": t_id,
                    "value": -value,
                    "note": note,
                }
                if t_id:
                    return Ok(f"Created transaction {result}")
                else:
                    return Err(f"No account registered to card: {card_id}")
        else:
            return Err(r.err_value)

    r = aiorun(_scan_and_add(value, device, note))
    if isinstance(r, Ok):
        pprint(r.ok_value)
    else:
        pprint(r.err_value)
