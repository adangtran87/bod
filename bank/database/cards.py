import aiosqlite
import enum

from pydantic import BaseModel
from typing import Optional

CREATE_CARDS_TABLE = """
CREATE TABLE IF NOT EXISTS cards (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    account_id INTEGER NULL,
    value FLOAT NULL,
    CONSTRAINT fk_accounts,
        FOREIGN KEY (account_id)
        REFERENCES accounts(id)
        ON DELETE SET NULL
);
"""

ADD_CARD_ACCOUNT = """
INSERT INTO cards (id, type, account_id)
VALUES (?, ?, ?);
"""

ADD_CARD_VALUE = """
INSERT INTO cards (id, type, value)
VALUES (?, ?, ?);
"""

GET_ALL_CARDS = """
SELECT * FROM cards;
"""

GET_CARDS_FOR_ACCOUNT = """
SELECT * FROM cards
WHERE cards.account_id = (?);
"""


class CardType(enum.Enum):
    UNKNOWN = "unknown"
    ACCOUNT = "account"
    VALUE = "value"


class Card(BaseModel):
    id: str
    type: CardType
    account_id: Optional[int]  # account_id
    value: Optional[float]


async def create_table(db: aiosqlite.Connection):
    await db.execute(CREATE_CARDS_TABLE)
    await db.commit()


async def add_card(db: aiosqlite.Connection, card: Card) -> int | None:
    card_id: int | None = None
    if card.type == CardType.ACCOUNT:
        cursor = await db.execute(
            ADD_CARD_ACCOUNT, [card.id, card.type.value, card.account_id]
        )
        card_id = cursor.lastrowid
    elif card.type == CardType.VALUE:
        cursor = await db.execute(
            ADD_CARD_VALUE, [card.id, card.type.value, card.value]
        )
        card_id = cursor.lastrowid
    else:
        raise NotImplementedError(f"add_card not implemented for {card.type}")
    await db.commit()

    return card_id


async def get_cards(db: aiosqlite.Connection) -> list[Card]:
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(GET_ALL_CARDS)
    rows = await cursor.fetchall()
    return [
        Card(
            id=row["id"],
            type=row["type"],
            account_id=row["account_id"],
            value=row["value"],
        )
        for row in rows
    ]


async def get_cards_for_account(db: aiosqlite.Connection, account_id: int):
    """Get all cards for a given account"""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(GET_CARDS_FOR_ACCOUNT, [account_id])
    rows = await cursor.fetchall()
    return [
        Card(
            id=row["id"],
            type=row["type"],
            account_id=row["account_id"],
            value=row["value"],
        )
        for row in rows
    ]
