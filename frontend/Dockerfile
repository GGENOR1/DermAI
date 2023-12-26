# Используем базовый образ с Node.js для React
FROM node:14

# Устанавливаем зависимости
WORKDIR /app
COPY package.json /app
COPY package-lock.json /app
RUN npm install

# Копируем все файлы фронтенда
COPY . /app

# Указываем команду для запуска приложения
CMD ["npm", "start"]