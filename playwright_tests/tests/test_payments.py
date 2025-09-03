import pytest
from config import ACCOUNT, BASE_URL
from infra.qiwi_api_client import QiwiApiClient


def test_creates_payment(api_client):
    payload = {
        "id": "test_payment_1",
        "sum": {"amount": 1.00, "currency": "643"},
        "paymentMethod": {"type": "Account", "accountId": "643"},
        "fields": {"account": ACCOUNT},
    }
    response = api_client.create_payment(99, payload)
    assert response.status in (200, 400)
    data = response.json()
    assert "transaction" in data or "errorCode" in data


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"id": "bad_1", "sum": {"amount": -1, "currency": "643"},
          "paymentMethod": {"type": "Account", "accountId": "643"},
          "fields": {"account": ACCOUNT}}, 400),

        ({"id": "bad_2", "sum": {"amount": 10, "currency": "840"},
          "paymentMethod": {"type": "Account", "accountId": "643"},
          "fields": {"account": ACCOUNT}}, 400),

        ({"id": "bad_3", "sum": {"amount": 10, "currency": "643"},
          "paymentMethod": {"type": "Unknown", "accountId": "643"},
          "fields": {"account": ACCOUNT}}, 400),

        ({"id": "bad_4", "sum": {"amount": 10, "currency": "643"},
          "paymentMethod": {"type": "Account", "accountId": "643"},
          "fields": {"account": "0000000000"}}, 400),
    ],
)
def test_gets_bad_request_error_on_incorrect_create_payment_request(
    api_client, payload, expected_status
):
    response = api_client.create_payment(99, payload)
    assert response.status == expected_status
    data = response.json()
    assert "errorCode" in data or "message" in data


def test_payment_unauthorized(playwright_context):
    client = QiwiApiClient(playwright_context, "invalid_token", BASE_URL)
    response = client.create_payment(99, {"id": "unauth_test"})
    assert response.status == 401
    client.dispose()


def test_payment_forbidden(playwright_context, TOKEN):
    fake_base_url = "https://api.qiwi.com/payout/v1/persons/9999999999"
    client = QiwiApiClient(playwright_context, TOKEN, fake_base_url)
    response = client.create_payment(99, {"id": "forbidden_test"})
    assert response.status == 403
    client.dispose()




