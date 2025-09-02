import os


ACCOUNT = os.getenv("QIWI_ACCOUNT")
TOKEN = os.getenv("QIWI_TOKEN")
BASE_URL = os.getenv("QIWI_BASE_URL")


def validate_config():
    if not ACCOUNT or not TOKEN or not BASE_URL:
        raise RuntimeError(
            "Не заданы переменные окружения: QIWI_ACCOUNT, QIWI_TOKEN, QIWI_BASE_URL"
        )
