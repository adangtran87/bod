import aiosqlite

import bank.database.accounts as accounts
import bank.database.cards as cards
import bank.database.transactions as transactions


async def get_account_info(
    db: aiosqlite.Connection, account: accounts.Account, num_transactions: int = 5
) -> dict:
    account_value = await transactions.get_total_for_account(db, account.id)
    account_cards = await cards.get_cards_for_account(db, account.id)
    account_transactions = await transactions.get_transactions_for_account(
        db, account.id
    )
    return {
        "account": account,
        "account_value": account_value,
        "num_cards": len(account_cards),
        "account_cards": [card.id for card in account_cards],
        "recent_transactions": account_transactions[:num_transactions],
    }
