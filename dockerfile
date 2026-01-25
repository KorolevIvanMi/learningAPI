FROM python:3.13-slim

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry (более стабильный способ)
RUN pip install --no-cache-dir poetry==2.2.1

# Настраиваем Poetry (не создавать виртуальное окружение)
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости
RUN poetry install --no-root

# Копируем весь код приложения
COPY . .

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]