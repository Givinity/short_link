# Shortlink Service

Сервис сокращения ссылок на FastAPI.

## Запуск

```bash
poetry install
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
