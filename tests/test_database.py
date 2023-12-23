import pytest

import bank.database.accounts as accounts
import bank.database.cards as cards


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


@pytest.mark.asyncio
async def test_create_cards(test_db):
    async with await test_db as db:
        await cards.create_table(db)
        card = cards.Card(
            id="cardid", type=cards.CardType.VALUE, account_id=None, value=10.0
        )
        await cards.add_card(db, card)
        data: list[cards.Card] = await cards.get_cards(db)

        assert len(data) == 1
        entry = data[0]
        assert entry.id == "cardid"
