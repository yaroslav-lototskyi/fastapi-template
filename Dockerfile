# Multi-stage build для оптимізації розміру образу
FROM python:3.11-slim as builder

# Встановити Poetry
RUN pip install poetry==1.7.0

# Налаштувати Poetry (не створювати venv, бо ми в контейнері)
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Копіювати файли залежностей
COPY pyproject.toml poetry.lock ./

# Встановити залежності
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# Production stage
FROM python:3.11-slim as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Копіювати venv з builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Копіювати код додатку
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

# Створити non-root користувача
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Відкрити порт
EXPOSE 8000

# Запустити додаток
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
