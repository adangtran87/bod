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
