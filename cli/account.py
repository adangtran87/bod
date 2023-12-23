from asyncio import run as aiorun
from pprint import pprint
from typing_extensions import Annotated
from typing import Optional

import typer
from result import Err, Ok, Result

import bank.database.accounts as accounts
import bank.database.database as database

from cli.utils import scan_card

app = typer.Typer()


@app.command()
def add(
    name: str,
    scan: Annotated[bool, typer.Option(help="Register a card")] = False,
    device: Annotated[
        str, typer.Option(help="Device location string")
    ] = "tty:USB0:pn532",
):
    async def _add_account(name: str, scan: bool, device: str) -> Result[dict, str]:
        async with await database.get_db() as db:
            # Check if card exists
            if await accounts.account_exists(db, None, name):
                return Err(f"Account {name} already exists")

            # Scan card
            card_id: str | None = None
            if scan:
                r = await scan_card(device)
                if isinstance(r, Ok):
                    card_id = r.ok_value
                else:
                    return Err(r.err_value)

            # Add account

            if card_id:
                account_id = await accounts.add_account_with_card(db, name, card_id)
            else:
                account_id = await accounts.add_account(db, name)

            return Ok(
                {
                    "account_id": account_id,
                    "card_id": card_id,
                }
            )

    r = aiorun(_add_account(name, scan, device))
    if isinstance(r, Ok):
        print(f"SUCCESS: {r.ok_value}")
    else:
        print(f"ERROR: {r.err_value}")


@app.command()
def delete(
    id: Annotated[Optional[int], typer.Option(help="account id")] = None,
    name: Annotated[Optional[str], typer.Option(help="account id")] = None,
):
    async def _delete_account(id: int | None, name: str | None) -> Result[None, str]:
        async with await database.get_db() as db:
            if not await accounts.account_exists(db, id, name):
                return Err(f"No account with id: {id} name: {name}")

            await accounts.delete_account(db, id, name)
            return Ok(None)

    aiorun(_delete_account(id, name))


@app.command()
def dump():
    async def _get_accounts() -> list[accounts.Account]:
        async with await database.get_db() as db:
            return await accounts.get_accounts(db)

    pprint(aiorun(_get_accounts()))


@app.command()
def scan(
    device: Annotated[
        str, typer.Option(help="Device location string")
    ] = "tty:USB0:pn532",
):
    async def _get_account_from_card(device) -> Result[accounts.Account, str]:
        r = await scan_card(device)
        if isinstance(r, Ok):
            card_id = r.ok_value
            async with await database.get_db() as db:
                account = await accounts.get_account_from_card(db, card_id=card_id)
                if account:
                    return Ok(account)
                else:
                    return Err(f"No account registered to card: {card_id}")
        else:
            return Err(r.err_value)

    r = aiorun(_get_account_from_card(device))
    if isinstance(r, Ok):
        pprint(r.ok_value)
    else:
        pprint(r.err_value)
