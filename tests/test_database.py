import pytest

import bank.database.accounts as accounts
import bank.database.cards as cards
import bank.database.transactions as transactions


@pytest.mark.asyncio
async def test_account_create(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        last_row = await accounts.add_account(db, "test")
        data: list[accounts.Account] = await accounts.get_accounts(db)

        assert len(data) == 1
        entry = data[0]
        assert entry.name == "test"
        assert entry.id == 1
        assert last_row == 1


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
        assert entry.id == card.id


@pytest.mark.asyncio
async def test_link_cards_to_account(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await cards.create_table(db)
        await accounts.add_account(db, "test")
        card = cards.Card(
            id="cardid", type=cards.CardType.ACCOUNT, account_id=1, value=None
        )
        await cards.add_card(db, card)

        data: list[cards.Card] = await cards.get_cards(db)
        assert len(data) == 1
        entry = data[0]
        assert entry.id == card.id
        assert entry.account_id == card.account_id


@pytest.mark.asyncio
async def test_get_account_by_name(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await accounts.add_account(db, "test2")
        await accounts.add_account(db, "test")
        data: accounts.Account | None = await accounts.get_account_by_name(db, "test")
        assert data is not None
        assert data.id == 2

        data: accounts.Account | None = await accounts.get_account_by_name(db, "foo")
        assert data is None


@pytest.mark.asyncio
async def test_delete_account(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await accounts.add_account(db, "test2")
        await accounts.add_account(db, "test")
        await accounts.delete_account(db, id=1)
        data: accounts.Account | None = await accounts.get_account_by_name(db, "test")
        assert data is not None
        assert data.name == "test"
        del_account: accounts.Account | None = await accounts.get_account_by_name(
            db, "foo"
        )
        assert del_account is None


@pytest.mark.asyncio
async def test_cursor_lastrowid(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await accounts.add_account(db, "test2")
        await accounts.add_account(db, "test")
        await accounts.delete_account(db, id=1)
        last_row = await accounts.add_account(db, "test3")
        assert last_row == 3


@pytest.mark.asyncio
async def test_account_exists(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await accounts.add_account(db, "test2")
        assert await accounts.account_exists(db, "test") is False
        assert await accounts.account_exists(db, 2) is False
        await accounts.add_account(db, "test")
        assert await accounts.account_exists(db, "test") is True
        assert await accounts.account_exists(db, 2) is True


@pytest.mark.asyncio
async def test_account_create_with_card(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await cards.create_table(db)
        account_id = await accounts.add_account_with_card(db, "test", "test_card_id")
        data_accounts = await accounts.get_accounts(db)
        assert len(data_accounts) == 1
        data_cards = await cards.get_cards(db)
        assert len(data_cards) == 1
        card = data_cards[0]
        assert card.account_id == account_id


@pytest.mark.asyncio
async def test_get_account_from_card_id(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await cards.create_table(db)
        await accounts.add_account(db, "test2")
        await accounts.add_account_with_card(db, "test", "test_card_id")
        account = await accounts.get_account_from_card(db, "test_card_id")

        assert account is not None
        assert account.id == 2
        assert account.name == "test"


@pytest.mark.asyncio
async def test_add_same_account_name(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        account_id = await accounts.add_account(db, "test2")
        assert account_id == 1
        account_id = await accounts.add_account(db, "test2")
        assert account_id is None


@pytest.mark.asyncio
async def test_add_transaction(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await transactions.create_table(db)
        t_id = await transactions.add_transaction(db, account_id=1, value=10.0, note="")
        assert t_id is None
        account_id = await accounts.add_account(db, "test")
        assert account_id is not None
        t_id = await transactions.add_transaction(
            db, account_id=account_id, value=10.0, note=""
        )
        assert t_id is not None
        assert t_id == 1


@pytest.mark.asyncio
async def test_get_transactions(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await transactions.create_table(db)
        account_id = await accounts.add_account(db, "test")
        assert account_id is not None
        _ = await transactions.add_transaction(
            db, account_id=account_id, value=10.0, note=""
        )
        _ = await transactions.add_transaction(
            db, account_id=account_id, value=20.0, note=""
        )
        _ = await transactions.add_transaction(
            db, account_id=account_id, value=1.0, note=""
        )
        data = await transactions.get_transactions(db)
        assert len(data) == 3
        assert data[0].value == 10.0
