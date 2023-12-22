import pytest

import bank.database.accounts as accounts


@pytest.mark.asyncio
async def test_account_create(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await accounts.add_account(db, "test")
        data: list[accounts.Account] = await accounts.get_accounts(db)

        assert len(data) == 1
        entry = data[0]
        assert entry.name == "test"
        assert entry.id == 1
