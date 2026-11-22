FROM python:3.12-slim

WORKDIR /app

ENV UV_PYTHON_DOWNLOADS=never \
    UV_NO_CACHE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Копируем uv из официального образа, фиксируя его версию.
COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /usr/local/bin/uv

# Этот слой меняется только при изменении зависимостей.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

# Копируем остальные файлы с учётом .dockerignore.
COPY . .

# Запускаем приложение обычным пользователем.
RUN useradd --create-home appuser
USER appuser

EXPOSE 8090

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8090"]