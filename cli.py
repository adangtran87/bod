import typer

import cli.card as card
import cli.account as account
import cli.database as database
import cli.transaction as transaction

app = typer.Typer()
app.add_typer(account.app, name="account")
app.add_typer(card.app, name="card")
app.add_typer(database.app, name="db")
app.add_typer(transaction.app, name="t")


if __name__ == "__main__":
    app()
