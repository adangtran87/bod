import aiosqlite
import pytest

import bank.database.accounts as accounts
import bank.database.cards as cards
import bank.database.transactions as transactions


@pytest.mark.asyncio
@pytest.fixture
async def test_db() -> aiosqlite.Connection:
    return aiosqlite.connect("file::memory:")


@pytest.mark.asyncio
@pytest.fixture
async def init_db(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await cards.create_table(db)
        await transactions.create_table(db)
        yield db


# TODO: Clean up database pattern
async def seeded_db():
    """Return a database connection for use as a dependency.
    This connection has the Row row factory automatically attached."""

    db = await aiosqlite.connect("file::memory:")
    # Provide a smarter version of the results. This keeps from having to unpack
    # tuples manually.
    db.row_factory = aiosqlite.Row

    await accounts.create_table(db)
    await cards.create_table(db)
    await transactions.create_table(db)

    await accounts.add_account(db, "test1")
    await accounts.add_account_with_card(db, "test2", "card1")

    try:
        yield db
    finally:
        await db.close()
