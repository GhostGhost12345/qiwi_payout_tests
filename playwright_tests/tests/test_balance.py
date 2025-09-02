import pytest
from config import ACCOUNT


def test_gets_balance(api_client):
    response = api_client.get_balance(ACCOUNT)
    print("RAW BALANCE:", response.text())
    assert response.status == 200
    data = response.json()
    assert "accounts" in data
    assert any(
        acc.get("balance", {}).get("amount", 0) >= 0 for acc in data["accounts"]
    )


def test_balance_not_found(api_client):
    response = api_client.get_balance("0000000000")
    print("RAW BALANCE NOT FOUND:", response.text())
    assert response.status == 404



