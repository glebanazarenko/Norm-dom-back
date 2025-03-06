#!/bin/sh
set -e

echo "Ожидание запуска PostgreSQL на db:5432..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL доступен."

echo "Применение миграций..."
aerich upgrade || { echo "Ошибка при обновлении миграций"; exit 1; }

echo "Инициализация базы данных..."
python src/init_db.py

echo "Запуск основного приложения..."
exec "$@"
