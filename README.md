# Лабораторная работа №5  
## Разработка автотестов для API Redfish с использованием PyTest

## Описание проекта

В данной лабораторной работе реализованы автоматизированные тесты для Redfish API платформы OpenBMC с использованием Python, PyTest и библиотеки Requests.

Redfish API используется для удалённого получения информации о системе и управления функциями BMC.

## Цель работы

Разработка автотестов REST API с использованием PyTest.

В рамках лабораторной реализованы проверки:

- авторизации через Redfish API;
- получения информации о системе;
- управления питанием системы;
- проверки наличия температурных сенсоров;
- проверки коллекции сенсоров Redfish.

## Используемые технологии

- Python 3.12
- PyTest
- Requests
- python-dotenv
- OpenBMC
- Redfish API

## Структура проекта

```
5_lab/
│
├── tests/
│   └── test_redfish.py
│
├── conftest.py
│
├── requirements.txt
│
├── .env
│
├── .gitignore
│
└── README.md
```

## Настройка окружения

Создание виртуального окружения:

```bash
python3 -m venv venv
```

Активация виртуального окружения:

```bash
source venv/bin/activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

## Настройка подключения

Параметры подключения к OpenBMC хранятся в файле `.env`.

Пример:

```env
REDFISH_URL=https://localhost:2443
REDFISH_USERNAME=root
REDFISH_PASSWORD=0penBmc
```

Файл `.env` исключён из Git через `.gitignore`.

## Реализованные тесты

### 1. Проверка авторизации Redfish

Проверяется:

- создание Redfish-сессии;
- успешность авторизации;
- получение токена X-Auth-Token.

Используемый API:

```
POST /redfish/v1/SessionService/Sessions
```

---

### 2. Проверка информации о системе

Проверяется получение данных о системе.

Используемый API:

```
GET /redfish/v1/Systems/system
```

Проверяется:

- код ответа HTTP 200;
- наличие поля Status;
- наличие поля PowerState.

---

### 3. Проверка управления питанием

Проверяется отправка команды включения системы.

Используемый API:

```
POST /redfish/v1/Systems/system/Actions/ComputerSystem.Reset
```

Передаваемые данные:

```json
{
    "ResetType": "On"
}
```

Проверяется успешность выполнения команды.

---

### 4. Проверка температуры CPU

Выполняется проверка наличия температурных сенсоров через Redfish API.

Используемый ресурс:

```
GET /redfish/v1/Chassis/chassis/Sensors
```

В виртуальной платформе OpenBMC Romulus физические CPU-сенсоры отсутствуют, поэтому тест корректно пропускается через `pytest.skip()`.

---

### 5. Проверка сенсоров Redfish

Проверяется наличие коллекции сенсоров и корректность ответа Redfish API.

---

## Реализация тестов

В проекте используется:

- `pytest.fixture` для создания общей Redfish-сессии;
- `requests.Session()` для выполнения API-запросов;
- `.env` для хранения настроек подключения;
- обработка отсутствующих ресурсов виртуальной платформы.

## Запуск тестов

Для запуска всех автотестов выполнить:

```bash
pytest -v
```

Пример успешного выполнения:

```
tests/test_redfish.py::test_authentication PASSED
tests/test_redfish.py::test_system_information PASSED
tests/test_redfish.py::test_power_on PASSED
tests/test_cpu_temperature SKIPPED
tests/test_cpu_sensor_match_ipmi PASSED

4 passed, 1 skipped
```

## Особенности работы

- Используется OpenBMC Redfish API.
- Подключение выполняется через HTTPS.
- Используется самоподписанный сертификат OpenBMC.
- Секретные данные не хранятся в исходном коде.
- Проверяется корректная работа API в виртуальной среде QEMU.

## Окружение выполнения

Тестирование выполнялось:

- Ubuntu Linux;
- QEMU;
- OpenBMC Romulus;
- Redfish API.

## Автор
Гриценко Андрей

Лабораторная работа №5  
Курс: Технологии программирования
