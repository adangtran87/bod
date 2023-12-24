from datetime import datetime
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
        data: accounts.Account | None = await accounts.get_account(db, "test")
        assert data is not None
        assert data.id == 2

        data: accounts.Account | None = await accounts.get_account(db, "foo")
        assert data is None


@pytest.mark.asyncio
async def test_get_account_by_id(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await accounts.add_account(db, "test2")
        await accounts.add_account(db, "test")
        data: accounts.Account | None = await accounts.get_account(db, 1)
        assert data is not None
        assert data.name == "test2"

        data: accounts.Account | None = await accounts.get_account(db, 3)
        assert data is None


@pytest.mark.asyncio
async def test_delete_account(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await accounts.add_account(db, "test2")
        await accounts.add_account(db, "test")
        await accounts.delete_account(db, account=1)
        data: accounts.Account | None = await accounts.get_account(db, "test")
        assert data is not None
        assert data.name == "test"
        del_account: accounts.Account | None = await accounts.get_account(db, "foo")
        assert del_account is None


@pytest.mark.asyncio
async def test_cursor_lastrowid(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await accounts.add_account(db, "test2")
        await accounts.add_account(db, "test")
        await accounts.delete_account(db, account=1)
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
        t = transactions.Transaction(
            id=0,  # not used
            date=datetime.now(),
            account_id=1,
            value=10.0,
            note=None,
        )
        t_id = await transactions.add_transaction(db, t)
        assert t_id is None
        account_id = await accounts.add_account(db, "test")
        assert account_id is not None
        t_id = await transactions.add_transaction(db, t)
        assert t_id is not None
        assert t_id != t.id
        assert t_id == 1


@pytest.mark.asyncio
async def test_get_transactions(test_db):
    async with await test_db as db:
        await accounts.create_table(db)
        await transactions.create_table(db)
        account_id = await accounts.add_account(db, "test")
        assert account_id is not None
        t = transactions.Transaction(
            id=0,  # not used
            date=datetime.now(),
            account_id=account_id,
            value=10.0,
            note=None,
        )
        _ = await transactions.add_transaction(db, t)
        t.value += 10.0
        _ = await transactions.add_transaction(db, t)
        t.value += 10.0
        _ = await transactions.add_transaction(db, t)
        data = await transactions.get_transactions(db)
        assert len(data) == 3
        assert data[0].value == 10.0
        assert data[0].id == 1
        assert data[1].value == 20.0
        assert data[1].id == 2
        assert data[2].value == 30.0
        assert data[2].id == 3


@pytest.mark.asyncio
async def test_add_transaction_from_card_id(init_db):
    async for db in init_db:
        account_id = await accounts.add_account_with_card(db, "test", "test_card_id")
        t = transactions.Transaction(
            id=0,  # not used
            date=datetime.now(),
            account_id=account_id,
            value=10.0,
            note=None,
        )
        t_id = await transactions.add_transaction_from_card_id(db, "test_card_id", t)
        assert t_id is not None
        assert t_id == 1

        data = await transactions.get_transactions(db)
        assert len(data) == 1
        row = data[0]
        assert row.account_id == t.account_id
        assert row.value == t.value
        assert row.note == t.note
        assert row.id != t.id


@pytest.mark.asyncio
async def test_get_transactions_for_account(init_db):
    async for db in init_db:
        account1 = await accounts.add_account(db, "test")
        assert account1 is not None
        t = transactions.Transaction(
            id=0,  # not used
            date=datetime.now(),
            account_id=account1,
            value=10.0,
            note=None,
        )
        t_id = await transactions.add_transaction(db, t)
        assert t_id is not None
        t2 = transactions.Transaction(
            id=0,  # not used
            date=datetime.now(),
            account_id=account1,
            value=20.0,
            note=None,
        )
        t_id = await transactions.add_transaction(db, t2)
        assert t_id is not None

        account2 = await accounts.add_account(db, "test2")
        assert account2 is not None
        t3 = transactions.Transaction(
            id=0,  # not used
            date=datetime.now(),
            account_id=account2,
            value=30.0,
            note=None,
        )
        t_id = await transactions.add_transaction(db, t3)
        assert t_id is not None

        data1 = await transactions.get_transactions_for_account(db, account_id=1)
        assert len(data1) == 2

        data2 = await transactions.get_transactions_for_account(db, account_id=account2)
        assert len(data2) == 1

        data_null = await transactions.get_transactions_for_account(db, account_id=100)
        assert len(data_null) == 0


@pytest.mark.asyncio
async def test_get_total_for_account(init_db):
    async for db in init_db:
        account1 = await accounts.add_account(db, "test")
        assert account1 is not None
        t = transactions.Transaction(
            id=0,  # not used
            date=datetime.now(),
            account_id=account1,
            value=10.0,
            note=None,
        )
        t_id = await transactions.add_transaction(db, t)
        assert t_id is not None
        t2 = transactions.Transaction(
            id=0,  # not used
            date=datetime.now(),
            account_id=account1,
            value=20.0,
            note=None,
        )
        t_id = await transactions.add_transaction(db, t2)
        assert t_id is not None

        account2 = await accounts.add_account(db, "test2")
        assert account2 is not None
        t3 = transactions.Transaction(
            id=0,  # not used
            date=datetime.now(),
            account_id=account2,
            value=30.0,
            note=None,
        )
        t_id = await transactions.add_transaction(db, t3)
        assert t_id is not None

        assert await transactions.get_total_for_account(db, account1) == 30
        assert await transactions.get_total_for_account(db, account2) == 30
        assert await transactions.get_total_for_account(db, 100) is None


@pytest.mark.asyncio
async def test_get_cards_for_account(init_db):
    async for db in init_db:
        acc = await accounts.add_account(db, "test")
        assert acc is not None
        c1 = cards.Card(
            id="card1", type=cards.CardType.ACCOUNT, account_id=acc, value=None
        )
        await cards.add_card(db, c1)
        c2 = cards.Card(
            id="card2", type=cards.CardType.ACCOUNT, account_id=acc, value=None
        )
        await cards.add_card(db, c2)
        c3 = cards.Card(
            id="card3", type=cards.CardType.ACCOUNT, account_id=acc, value=None
        )
        await cards.add_card(db, c3)

        data = await cards.get_cards_for_account(db, account_id=acc)
        assert len(data) == 3

        assert data[0] == c1
        assert data[1] == c2
        assert data[2] == c3
