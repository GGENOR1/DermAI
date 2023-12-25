FROM ubuntu:latest
LABEL authors="Ruslan"
# Используем базовый образ Node.js
FROM node:14

# Устанавливаем директорию приложения в контейнере
WORKDIR /app

# Копируем файлы зависимостей и устанавливаем их
COPY package.json /app/
COPY package-lock.json /app/
RUN npm install

# Копируем остальные файлы проекта в директорию приложения
COPY . /app/

# Собираем приложение React
RUN npm run build

# Определяем команду для запуска сервера разработки React
CMD ["npm", "start"]
