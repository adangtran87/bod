import aiosqlite
import enum
from string import Template

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
VALUES ("${id}", "${type}", ${account_id});
"""

ADD_CARD_VALUE = """
INSERT INTO cards (id, type, value)
VALUES ("${id}", "${type}", ${value});
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


ADD_CARD_SQL = {
    CardType.ACCOUNT: ADD_CARD_ACCOUNT,
    CardType.VALUE: ADD_CARD_VALUE,
}


class Card(BaseModel):
    id: str
    type: CardType
    account_id: Optional[int]  # account_id
    value: Optional[float]


async def create_table(db: aiosqlite.Connection):
    await db.execute(CREATE_CARDS_TABLE)
    await db.commit()


async def add_card(db: aiosqlite.Connection, card: Card):
    fields = card.model_dump()
    fields["type"] = card.type.value
    sql = Template(ADD_CARD_SQL[card.type])
    cmd = sql.safe_substitute(fields)
    await db.execute(cmd)
    await db.commit()


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
