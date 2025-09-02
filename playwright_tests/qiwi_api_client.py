import json


class QiwiApiClient:
    def __init__(self, playwright, token: str, base_url: str):
        self.context = playwright.request.new_context(
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        self.base_url = base_url

    def dispose(self):
        self.context.dispose()

    def get_balance(self, account: str):
        return self.context.get(
            f"{self.base_url}/funding-sources/v2/persons/{account}/accounts"
        )

    def create_payment(self, provider_id: int, payload: dict):
        return self.context.post(
            f"{self.base_url}/sinap/api/v2/terms/{provider_id}/payments",
            data=json.dumps(payload),
        )
