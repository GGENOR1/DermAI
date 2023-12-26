# Используем базовый образ Python
FROM python:3.11
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Копируем все файлы приложения
COPY backend /app/backend

COPY app_entrypoint.sh /app
CMD [ "./app_entrypoint.sh" ]

#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]