import aiosqlite

from .database import DB_FILE

CREATE_ACCOUNT_TABLE = """
CREATE TABLE IF NOT EXISTS account (
    id INT PRIMARY_KEY,
    name TEXT NOT NULL
);
"""


async def create_account_table():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(CREATE_ACCOUNT_TABLE)
        await db.commit()
