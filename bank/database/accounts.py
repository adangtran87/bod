import aiosqlite

from pydantic import BaseModel
from string import Template

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


class Account(BaseModel):
    id: int
    name: str


async def create_table(db: aiosqlite.Connection):
    await db.execute(CREATE_ACCOUNTS_TABLE)
    await db.commit()


async def add_account(db: aiosqlite.Connection, name: str):
    cmd = ADD_ACCOUNT.safe_substitute({"name": name})
    await db.execute(cmd)
    await db.commit()


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
