# Используем официальный образ Python как базовый
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY .. /app/

# Открываем порт для приложения
EXPOSE 8000

# Команда для запуска Django-приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]