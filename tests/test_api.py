from conftest import seeded_db

from fastapi.testclient import TestClient

import bank.database.accounts as accounts

from bank.server.server import app
from bank.database.database import rest_db
from bank.models.schemas import AccountList

app.dependency_overrides[rest_db] = seeded_db
client = TestClient(app)


def test_account_create():
    """Create an account using /account/create"""
    acc = accounts.Account(id=0, name="test3")

    response = client.post("/account/create/", json=acc.model_dump())
    assert response.status_code == 200
    assert response.json() == {"id": 3, "name": "test3"}


def test_account_create_already_existing():
    """Create an account with a name that already exists"""
    response = client.get("/accounts/")
    acc = accounts.Account(id=0, name="test1")

    response = client.post("/account/create/", json=acc.model_dump())
    assert response.status_code == 409


def test_account_info():
    account_id = 1
    response = client.get(f"/account/info/{account_id}")
    assert response.status_code == 200
    info = response.json()

    assert info["account"] == accounts.Account(id=account_id, name="test1").model_dump()
    assert info["card_ids"] == ["card1"]
    assert len(info["transactions"]) == 2
    assert info["transactions"][0]["date"] > info["transactions"][1]["date"]
