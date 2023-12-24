from asyncio import run as aiorun
from pprint import pprint
from typing_extensions import Annotated
from typing import Optional

import typer
from result import Err, Ok, Result

import bank.database.accounts as accounts
import bank.database.database as database
import bank.database.utils as db_utils

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
            if await accounts.account_exists(db, name):
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
    async def _delete_account(search: int | str) -> Result[None, str]:
        async with await database.get_db() as db:
            if not await accounts.account_exists(db, search):
                return Err(f"No account found when searching for {search}")

            await accounts.delete_account(db, search)
            return Ok(None)

    if id:
        aiorun(_delete_account(id))
    elif name:
        aiorun(_delete_account(name))
    else:
        print("ERROR: Need to provide --id or --name")


@app.command()
def dump():
    async def _get_accounts() -> list[accounts.Account]:
        async with await database.get_db() as db:
            return await accounts.get_accounts(db)

    pprint(aiorun(_get_accounts()))


@app.command()
def info(
    id: Annotated[Optional[int], typer.Option(help="Account ID")] = None,
    name: Annotated[Optional[str], typer.Option(help="Account Name")] = None,
    scan: Annotated[bool, typer.Option(help="Register a card")] = False,
    device: Annotated[
        str, typer.Option(help="Device location string")
    ] = "tty:USB0:pn532",
):
    async def _get_account_info(
        id: int | None, name: str | None, scan: bool, device
    ) -> Result[dict, str]:
        async with await database.get_db() as db:
            account = None
            account_info: int | str
            if id:
                account = await accounts.get_account(db, id)
                account_info = id
            elif name:
                account = await accounts.get_account(db, name)
                account_info = name
            elif scan:
                r = await scan_card(device)
                if isinstance(r, Ok):
                    card_id = r.ok_value
                else:
                    return Err(r.err_value)
                account = await accounts.get_account_from_card(db, card_id)
                account_info = f"card_id: {card_id}"
            else:
                return Err("No identifier to find an account")

            if account:
                return Ok(await db_utils.get_account_info(db, account))
            else:
                return Err(f"Account {account_info} not found")

    """
    Get information about an account
    
    Identify an account by using --id or --name or --scan a card
    """
    if (id and name) or (id and scan) or (name and scan):
        print("Only use **one of** --id, --name, --scan")
        return

    if not (id or name or scan):
        print("Please use **one** of --id, n--name, --scan")
        return

    r = aiorun(_get_account_info(id, name, scan, device))
    if isinstance(r, Ok):
        pprint(r.ok_value)
    else:
        pprint(f"ERROR: {r.err_value}")


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
