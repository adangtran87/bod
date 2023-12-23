import aiosqlite

from pydantic import BaseModel
from string import Template
from typing import Optional

CREATE_ACCOUNTS_TABLE = """
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
"""

ADD_ACCOUNT = Template(
    """
INSERT INTO accounts (name) VALUES ("${name}");
"""
)

GET_ALL_ACCOUNTS = """
SELECT * FROM accounts;
"""

GET_ACCOUNT_BY_NAME = Template(
    """
SELECT * FROM accounts WHERE (name = "${name}");
"""
)

DELETE_ACCOUNT_BY_NAME = Template(
    """
DELETE FROM accounts WHERE (name = "${name}");
"""
)

DELETE_ACCOUNT_BY_ID = Template(
    """
DELETE FROM accounts WHERE (id = ${id});
"""
)


class Account(BaseModel):
    id: int
    name: str


async def create_table(db: aiosqlite.Connection):
    await db.execute(CREATE_ACCOUNTS_TABLE)
    await db.commit()


async def add_account(db: aiosqlite.Connection, name: str) -> Optional[int]:
    cmd = ADD_ACCOUNT.safe_substitute({"name": name})
    cursor = await db.execute(cmd)
    await db.commit()
    return cursor.lastrowid


async def get_accounts(db: aiosqlite.Connection) -> list[Account]:
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(GET_ALL_ACCOUNTS)
    rows = await cursor.fetchall()
    return [Account(id=row["id"], name=row["name"]) for row in rows]


async def get_account_by_name(db: aiosqlite.Connection, name: str):
    db.row_factory = aiosqlite.Row
    cmd = GET_ACCOUNT_BY_NAME.safe_substitute({"name": name})
    cursor = await db.execute(cmd)
    rows = await cursor.fetchall()
    return [Account(id=row["id"], name=row["name"]) for row in rows]


async def delete_account(
    db: aiosqlite.Connection, id: Optional[int] = None, name: Optional[str] = None
):
    if id:
        cmd = DELETE_ACCOUNT_BY_ID.safe_substitute({"id": id})
    elif name:
        cmd = DELETE_ACCOUNT_BY_NAME.safe_substitute({"name": name})
    else:
        raise RuntimeError("No arguments sent to delete_account")

    await db.execute(cmd)
    await db.commit()
