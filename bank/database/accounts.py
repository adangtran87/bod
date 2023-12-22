import aiosqlite

from pydantic import BaseModel

CREATE_ACCOUNTS_TABLE = """
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
"""

ADD_ACCOUNT = """
INSERT INTO accounts (name) VALUES ("{name}");
"""

GET_ALL_ACCOUNTS = """
SELECT * FROM accounts;
"""


class Account(BaseModel):
    id: int
    name: str


async def create_table(db: aiosqlite.Connection):
    await db.execute(CREATE_ACCOUNTS_TABLE)
    await db.commit()


async def add_account(db: aiosqlite.Connection, name: str):
    await db.execute(ADD_ACCOUNT.format(name=name))
    await db.commit()


async def get_accounts(db: aiosqlite.Connection) -> list[Account]:
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(GET_ALL_ACCOUNTS)
    rows = await cursor.fetchall()
    return [Account(id=row["id"], name=row["name"]) for row in rows]
