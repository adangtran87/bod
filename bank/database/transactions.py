from datetime import datetime
import aiosqlite

from pydantic import BaseModel

from bank.database.accounts import account_exists, get_account_from_card

CREATE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    date DATETIME NOT NULL,
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
INSERT INTO transactions (account_id, date, value, note)
VALUES (?, ?, ?, ?);
"""

GET_ALL_TRANSACTIONS = """
SELECT * from transactions
ORDER BY date DESC;
"""

GET_TRANSACTIONS_FOR_ACCOUNT = """
SELECT t.id, t.date, t.value, t.account_id, t.note
FROM transactions AS t
INNER JOIN accounts AS a
ON a.id == t.account_id
WHERE t.account_id == ?
ORDER BY date DESC;
"""

GET_TOTAL_FOR_ACCOUNT = """
SELECT SUM(t.value)
FROM transactions AS t
INNER JOIN accounts AS a
ON a.id == t.account_id
WHERE t.account_id == ?;
"""


class Transaction(BaseModel):
    id: int
    date: datetime
    value: float
    account_id: int | None
    note: str | None


async def create_table(db: aiosqlite.Connection):
    await db.execute(CREATE_TRANSACTIONS_TABLE)
    await db.commit()


async def add_transaction(db: aiosqlite.Connection, t: Transaction) -> int | None:
    """Add transaction to account if account exists, else do nothing"""
    if t.account_id is None:
        return None
    if not await account_exists(db, account=t.account_id):
        return None
    cursor = await db.execute(ADD_TRANSACTION, [t.account_id, t.date, t.value, t.note])
    await db.commit()
    return cursor.lastrowid


async def get_transactions(db: aiosqlite.Connection) -> list[Transaction]:
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(GET_ALL_TRANSACTIONS)
    rows = await cursor.fetchall()
    return [
        Transaction(
            id=row["id"],
            date=row["date"],
            value=row["value"],
            account_id=row["account_id"],
            note=row["note"],
        )
        for row in rows
    ]


async def add_transaction_from_card_id(
    db: aiosqlite.Connection, card_id: str, t: Transaction
) -> int | None:
    """
    Look up account from card and add a transaction

    t.id is not used when creating a transaction
    """
    account = await get_account_from_card(db, card_id)
    if account:
        t.account_id = account.id
        return await add_transaction(db, t)
    else:
        return None


async def get_transactions_for_account(
    db: aiosqlite.Connection, account_id: int
) -> list[Transaction]:
    """
    Get all transactions for an account
    """
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(GET_TRANSACTIONS_FOR_ACCOUNT, [account_id])
    rows = await cursor.fetchall()
    return [
        Transaction(
            id=row["id"],
            date=row["date"],
            value=row["value"],
            account_id=row["account_id"],
            note=row["note"],
        )
        for row in rows
    ]


async def get_total_for_account(
    db: aiosqlite.Connection, account_id: int
) -> float | None:
    """Sum up all transactions for account"""
    cursor = await db.execute(GET_TOTAL_FOR_ACCOUNT, [account_id])
    row = await cursor.fetchone()
    if row:
        return row[0]
    else:
        return None
