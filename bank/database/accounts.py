import aiosqlite

from .database import DB_FILE
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


async def create_table():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(CREATE_ACCOUNTS_TABLE)
        await db.commit()


async def add_account(name: str):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(ADD_ACCOUNT.format(name=name))
        await db.commit()


async def get_accounts() -> list[Account]:
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(GET_ALL_ACCOUNTS)
        rows = await cursor.fetchall()
        return [Account(id=row["id"], name=row["name"]) for row in rows]
