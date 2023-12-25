import aiosqlite
from datetime import datetime
import pytest

import bank.database.accounts as accounts
import bank.database.cards as cards
import bank.database.transactions as transactions


TEST_DB = "file::memory:"


@pytest.fixture
async def test_db() -> aiosqlite.Connection:
    return aiosqlite.connect(TEST_DB)


@pytest.fixture
async def init_db():
    """Return a database connection for use as a dependency.
    This connection has the Row row factory automatically attached."""

    db = await aiosqlite.connect(TEST_DB)
    # Provide a smarter version of the results. This keeps from having to unpack
    # tuples manually.
    db.row_factory = aiosqlite.Row

    await accounts.create_table(db)
    await cards.create_table(db)
    await transactions.create_table(db)

    try:
        yield db
    finally:
        await db.close()


# TODO: Clean up database pattern
async def seeded_db():
    """Return a database connection for use as a dependency.
    This connection has the Row row factory automatically attached."""

    db = await aiosqlite.connect(TEST_DB)
    # Provide a smarter version of the results. This keeps from having to unpack
    # tuples manually.
    db.row_factory = aiosqlite.Row

    await accounts.create_table(db)
    await cards.create_table(db)
    await transactions.create_table(db)

    account1 = await accounts.add_account(db, "test1")
    account2 = await accounts.add_account_with_card(db, "test2", "card2")

    c1 = cards.Card(
        id="card1", type=cards.CardType.ACCOUNT, account_id=account1, value=None
    )
    _ = await cards.add_card(db, c1)

    t1 = transactions.Transaction(
        id=0,  # not used
        date=datetime.now(),
        account_id=account1,
        value=10.0,
        note=None,
    )
    t_id = await transactions.add_transaction(db, t1)
    t2 = transactions.Transaction(
        id=0,  # not used
        date=datetime.now(),
        account_id=account1,
        value=20.0,
        note=None,
    )
    t_id = await transactions.add_transaction(db, t2)

    t1 = transactions.Transaction(
        id=0,  # not used
        date=datetime.now(),
        account_id=account2,
        value=20,
        note=None,
    )
    t_id = await transactions.add_transaction(db, t1)
    assert t_id is not None
    t2 = transactions.Transaction(
        id=0,  # not used
        date=datetime.now(),
        account_id=account2,
        value=-10,
        note=None,
    )
    t_id = await transactions.add_transaction(db, t2)
    assert t_id is not None

    try:
        yield db
    finally:
        await db.close()
