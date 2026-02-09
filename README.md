# Shortlink Service

Сервис сокращения ссылок на FastAPI.

## Запуск

```bash
poetry install --no-root
poetry run uvicorn main:app --reload
```

## API

- `POST /api/v1/shorten` — создать короткую ссылку
- `GET /api/v1/home` — список всех ссылок
- `GET /{code}` — редирект на оригинальный URL

## Тесты

```bash
poetry run pytest -v
```

## Линтинг и форматирование

```bash
# Проверка кода
poetry run ruff check .

# Автоисправление
poetry run ruff check . --fix

# Форматирование
poetry run ruff format .
```
