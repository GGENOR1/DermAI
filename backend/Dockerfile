
FROM python:3.11


WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем остальные файлы проекта в директорию приложения
COPY ../../fastapi-react/backend/app /code/

# Запускаем FastAPI сервер при запуске контейнера
ENTRYPOINT ["uvicorn", "api:app", "--host", "0.0.0.0" ]
