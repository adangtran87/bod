from conftest import seeded_db

from fastapi.testclient import TestClient

from bank.server.server import app
from bank.database.database import rest_db
from bank.models.schemas import AccountList

app.dependency_overrides[rest_db] = seeded_db
client = TestClient(app)


def test_get_all_accounts():
    response = client.get("/accounts/")
    assert response.status_code == 200
    print(response.json())
    data = AccountList.model_validate(response.json())
    assert len(data.accounts) == 2
    assert data.model_dump() == {
        "accounts": [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]
    }


def test_get_account_by_id():
    response = client.get("/accounts/?id=1")
    assert response.status_code == 200
    data = AccountList.model_validate(response.json())
    assert data.model_dump() == {"accounts": [{"id": 1, "name": "test1"}]}

    response = client.get("/accounts/?id=2")
    assert response.status_code == 200
    data = AccountList.model_validate(response.json())
    assert data.model_dump() == {"accounts": [{"id": 2, "name": "test2"}]}


def test_get_account_by_name():
    response = client.get("/accounts/?name=test1")
    assert response.status_code == 200
    data = AccountList.model_validate(response.json())
    assert data.model_dump() == {"accounts": [{"id": 1, "name": "test1"}]}
    response = client.get("/accounts/?name=test2")
    assert response.status_code == 200
    data = AccountList.model_validate(response.json())
    assert data.model_dump() == {"accounts": [{"id": 2, "name": "test2"}]}


def test_get_account_by_id_name():
    """
    Expecatation is that id is parsed first so the name is ignored.
    """
    response = client.get("/accounts/?id=1&name=test2")
    assert response.status_code == 200
    data = AccountList.model_validate(response.json())
    assert data.model_dump() == {"accounts": [{"id": 1, "name": "test1"}]}
