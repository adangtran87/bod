import aiosqlite

from pydantic import BaseModel

from bank.database.accounts import account_exists

CREATE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    value FLOAT NOT NULL,
    account_id INTEGER NULL,
    note TEXT NULL,
    CONSTRAINT fk_transaction_accounts,
        FOREIGN KEY (account_id)
        REFERENCES accounts(id)
        ON DELETE SET NULl
);
"""

ADD_TRANSACTION = """
INSERT INTO transactions (account_id, value, note)
VALUES (?, ?, ?);
"""


class Transaction(BaseModel):
    id: int
    value: float
    account_id: int | None
    note: str | None


async def create_table(db: aiosqlite.Connection):
    await db.execute(CREATE_TRANSACTIONS_TABLE)
    await db.commit()


async def add_transaction(
    db: aiosqlite.Connection, account_id: int, value: float, note: str | None = None
) -> int | None:
    """Add transaction to account if account exists, else do nothing"""
    if not await account_exists(db, search=account_id):
        return None
    cursor = await db.execute(ADD_TRANSACTION, [account_id, value, note])
    await db.commit()
    return cursor.lastrowid
