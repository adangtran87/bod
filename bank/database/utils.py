import aiosqlite
from pydantic import BaseModel
from result import Ok, Err, Result

import bank.database.accounts as accounts
import bank.database.cards as cards
import bank.database.transactions as transactions


class AccountInfo(BaseModel):
    account: accounts.Account
    value: float
    card_ids: list[str]
    transactions: list[transactions.Transaction]


async def get_account_info(
    db: aiosqlite.Connection, account_id: int, num_transactions: int = 5
) -> Result[AccountInfo, str]:
    account = await accounts.get_account(db, account_id)
    if not account:
        return Err(f"Account {account_id} not found")

    account_value = await transactions.get_total_for_account(db, account.id)
    account_cards = await cards.get_cards_for_account(db, account.id)
    account_transactions = await transactions.get_transactions_for_account(
        db, account.id
    )
    return Ok(
        AccountInfo(
            account=account,
            value=account_value if account_value else 0.0,
            card_ids=[card.id for card in account_cards],
            transactions=account_transactions[:num_transactions],
        )
    )
