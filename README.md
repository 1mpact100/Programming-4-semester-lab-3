# Лабораторная работа 3: Currency Tracker API

Асинхронный REST API на FastAPI и SQLAlchemy для регистрации пользователей,
подписок на валюты и хранения курсов, полученных из XML API Центрального банка
РФ.

## Возможности

- CRUD пользователей с проверкой уникальности `username` и `email`;
- подписка и отписка пользователя от валюты;
- загрузка списка валют и истории курсов из ЦБ РФ;
- получение последнего сохранённого курса валюты;
- SQLite через асинхронный драйвер `aiosqlite`;
- автоматическая документация Swagger.

## Запуск

Требуется Python 3.10 или новее.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

После запуска:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- проверка состояния: <http://127.0.0.1:8000/>

Таблицы автоматически создаются в `app.db` при запуске приложения. Путь к БД и
URL ЦБ можно изменить переменными окружения:

```bash
DATABASE_URL=sqlite+aiosqlite:///./custom.db uvicorn app.main:app
CBR_DAILY_URL=https://example.test/rates.xml uvicorn app.main:app
```

## Основные эндпоинты

| Метод | Путь | Назначение |
|---|---|---|
| `POST` | `/users/` | создать пользователя |
| `GET` | `/users/` | получить всех пользователей |
| `GET` | `/users/{user_id}` | получить пользователя и его подписки |
| `PUT` | `/users/{user_id}` | обновить пользователя |
| `DELETE` | `/users/{user_id}` | удалить пользователя |
| `POST` | `/subscriptions/` | подписаться на валюту |
| `DELETE` | `/subscriptions/` | отписаться от валюты |
| `GET` | `/currencies/` | получить сохранённые валюты |
| `POST` | `/currencies/update` | загрузить валюты и курсы из ЦБ |
| `GET` | `/currencies/{code}/rate` | получить последний курс |

Сначала вызовите `POST /currencies/update`, чтобы заполнить список доступных
валют. Для подписки можно передать либо `currency_code`, либо `currency_id`:

```json
{
  "user_id": 1,
  "currency_code": "USD"
}
```

## Тесты

```bash
pip install -r requirements-dev.txt
pytest
```
