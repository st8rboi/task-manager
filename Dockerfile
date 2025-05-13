FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Устанавливаем переменные окружения для Flask
ENV FLASK_APP=app/routes/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Открываем порт
EXPOSE 5000

# Команда запуска
CMD ["flask", "run"]