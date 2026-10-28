import os
import pytest
import requests

from dotenv import load_dotenv


# Загружаем настройки из .env
load_dotenv()


REDFISH_URL = os.getenv(
    "REDFISH_URL",
    "https://localhost:2443"
)

USERNAME = os.getenv(
    "REDFISH_USERNAME",
    "root"
)

PASSWORD = os.getenv(
    "REDFISH_PASSWORD",
    "0penBmc"
)


@pytest.fixture
def redfish_session():
    """
    Создание общей Redfish-сессии.

    Используется всеми тестами:
    - авторизация;
    - получение информации о системе;
    - управление питанием.
    """

    session = requests.Session()

    # В OpenBMC используется самоподписанный сертификат
    session.verify = False

    # Убираем предупреждения SSL
    requests.packages.urllib3.disable_warnings()


    # Авторизация через Redfish SessionService
    response = session.post(
        f"{REDFISH_URL}/redfish/v1/SessionService/Sessions",
        json={
            "UserName": USERNAME,
            "Password": PASSWORD
        }
    )


    assert response.status_code in (
        200,
        201
    ), (
        f"Ошибка авторизации Redfish: "
        f"{response.status_code}"
    )


    # Redfish возвращает токен X-Auth-Token
    token = response.headers.get(
        "X-Auth-Token"
    )


    if token:
        session.headers.update(
            {
                "X-Auth-Token": token
            }
        )


    yield session


    # Закрываем сессию после теста
    session.close()
