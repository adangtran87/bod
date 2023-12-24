from asyncio import run as aiorun
from datetime import datetime
from pprint import pprint
from typing_extensions import Annotated
from typing import Optional

import typer
from result import Err, Ok, Result

import bank.database.accounts as accounts
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


async def _add_transaction(
    id: int | None,
    name: str | None,
    scan: bool,
    value: float,
    device: str,
    note: str | None,
) -> Result[str, str]:
    """
    Add a transaction to an account using either id, name or scanning a card
    """
    async with await database.get_db() as db:
        t = transactions.Transaction(
            id=0, date=datetime.now(), value=value, account_id=0, note=note
        )
        if id:
            account = await accounts.get_account(db, id)
            if account:
                t.account_id = account.id
                t_id = await transactions.add_transaction(db, t)
            else:
                return Err(f"Account {id} does not exist")
        elif name:
            account = await accounts.get_account(db, name)
            if account:
                t.account_id = account.id
                t_id = await transactions.add_transaction(db, t)
            else:
                return Err(f"Account {name} does not exist")
        elif scan:
            r = await scan_card(device)
            if isinstance(r, Ok):
                card_id = r.ok_value
                t_id = await transactions.add_transaction_from_card_id(
                    db, card_id=card_id, t=t
                )
                if not t_id:
                    return Err(f"No account registered to card: {card_id}")
            else:
                return Err(r.err_value)
        else:
            raise RuntimeError("No way to find account")

        result = {
            "id": t_id,
            "value": value,
            "note": note,
        }
        if t_id:
            return Ok(f"Created transaction {result}")
        else:
            return Err("Failed to create transaction")


@app.command()
def add(
    value: Annotated[float, typer.Argument(help="Transaction value")],
    id: Annotated[Optional[int], typer.Option(help="Account ID")] = None,
    name: Annotated[Optional[str], typer.Option(help="Account name")] = None,
    scan: Annotated[bool, typer.Option(help="Scan an account card")] = False,
    device: Annotated[
        str, typer.Option(help="Device location string")
    ] = "tty:USB0:pn532",
    note: Annotated[Optional[str], typer.Option(help="Transaction note")] = None,
):
    """Add a transaction "to a card"

    This assumes the user has run "cli account add --scan" prior
    to create an account associated with a card
    """

    if (id and name) or (name and scan) or (id and scan):
        print("ERROR: Only one of id, name, or scan can be provided")
        return

    if not (id or name or scan):
        print("ERROR: One of id, name, or scan must be provided")
        return

    r = aiorun(_add_transaction(id, name, scan, value, device, note))
    if isinstance(r, Ok):
        pprint(r.ok_value)
    else:
        pprint(r.err_value)


@app.command()
def sub(
    value: Annotated[float, typer.Argument(help="Value to subtract")],
    id: Annotated[Optional[int], typer.Option(help="Account ID")] = None,
    name: Annotated[Optional[str], typer.Option(help="Account name")] = None,
    scan: Annotated[bool, typer.Option(help="Scan an account card")] = False,
    device: Annotated[
        str, typer.Option(help="Device location string")
    ] = "tty:USB0:pn532",
    note: Annotated[Optional[str], typer.Option(help="Transaction note")] = None,
):
    """Add a transaction "to a card"

    This assumes the user has run "cli account add --scan" prior
    to create an account associated with a card
    """
    r = aiorun(_add_transaction(id, name, scan, -value, device, note))
    if isinstance(r, Ok):
        pprint(r.ok_value)
    else:
        pprint(r.err_value)
