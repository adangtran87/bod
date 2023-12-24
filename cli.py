import typer

import cli.card as card
import cli.account as account
import cli.database as database
import cli.transaction as transaction

from bank.version import VERSION

app = typer.Typer()
app.add_typer(account.app, name="a", help="Account commands")
app.add_typer(account.app, name="account", help="Account commands")
app.add_typer(card.app, name="card", help="Card commands")
app.add_typer(database.app, name="db", help="Database commands")
app.add_typer(transaction.app, name="t", help="Transaction commands")
app.add_typer(transaction.app, name="transaction", help="Transaction commands")


@app.command()
def version():
    """Show the version of the application."""
    typer.echo(VERSION)


if __name__ == "__main__":
    app()
