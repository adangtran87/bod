import aiosqlite

from pydantic import BaseModel
from typing import Optional

import bank.database.cards as cards

CREATE_ACCOUNTS_TABLE = """
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
"""

ADD_ACCOUNT = """
INSERT INTO accounts (name)
VALUES (?);
"""

GET_ALL_ACCOUNTS = """
SELECT * FROM accounts;
"""

GET_ACCOUNT_BY_ID = """
SELECT * FROM accounts
WHERE (id = ?);
"""

GET_ACCOUNT_BY_NAME = """
SELECT * FROM accounts
WHERE (name = ?);
"""

GET_ACCOUNT_BY_CARD = """
SELECT accounts.id, accounts.name
FROM accounts
INNER JOIN cards ON cards.account_id == accounts.id
WHERE cards.id == ?;
"""

DELETE_ACCOUNT_BY_NAME = """
DELETE FROM accounts WHERE (name = ?);
"""

DELETE_ACCOUNT_BY_ID = """
DELETE FROM accounts WHERE (id = ?);
"""


class Account(BaseModel):
    id: int
    name: str


async def create_table(db: aiosqlite.Connection):
    await db.execute(CREATE_ACCOUNTS_TABLE)
    await db.commit()


async def add_account(db: aiosqlite.Connection, name: str) -> Optional[int]:
    try:
        cursor = await db.execute(ADD_ACCOUNT, [name])
        await db.commit()
        return cursor.lastrowid
    # Unique constraint failed
    except aiosqlite.IntegrityError:
        return None


async def add_account_with_card(
    db: aiosqlite.Connection, name: str, card_id: str
) -> Optional[int]:
    account_id = await add_account(db, name)
    card = cards.Card(
        id=card_id,
        type=cards.CardType.ACCOUNT,
        account_id=account_id,
        value=None,
    )
    await cards.add_card(db, card)
    return account_id


async def get_accounts(db: aiosqlite.Connection) -> list[Account]:
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(GET_ALL_ACCOUNTS)
    rows = await cursor.fetchall()
    return [Account(id=row["id"], name=row["name"]) for row in rows]


async def get_account(db: aiosqlite.Connection, account: int | str) -> Account | None:
    """
    Get account by id or name
    """
    db.row_factory = aiosqlite.Row
    if isinstance(account, int):
        cursor = await db.execute(GET_ACCOUNT_BY_ID, [account])
    else:
        cursor = await db.execute(GET_ACCOUNT_BY_NAME, [account])

    row = await cursor.fetchone()
    if row:
        return Account(id=row["id"], name=row["name"])
    else:
        return None


async def get_account_from_card(
    db: aiosqlite.Connection, card_id: str
) -> Account | None:
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(GET_ACCOUNT_BY_CARD, [card_id])
    row = await cursor.fetchone()
    if row:
        return Account(id=row["id"], name=row["name"])
    else:
        return None


async def account_exists(db: aiosqlite.Connection, account: int | str) -> int:
    """
    Check if an account exists by id[int] or name[str]
    """
    db.row_factory = aiosqlite.Row
    if isinstance(account, int):
        cursor = await db.execute(GET_ACCOUNT_BY_ID, [account])
    else:
        cursor = await db.execute(GET_ACCOUNT_BY_NAME, [account])
    row = await cursor.fetchone()
    if row:
        return True
    return False


async def delete_account(db: aiosqlite.Connection, account: int | str):
    if isinstance(account, int):
        await db.execute(DELETE_ACCOUNT_BY_ID, [account])
    else:
        await db.execute(DELETE_ACCOUNT_BY_NAME, [account])
    await db.commit()
