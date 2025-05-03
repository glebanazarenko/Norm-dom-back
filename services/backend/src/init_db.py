import asyncio
import json
from decimal import Decimal

from tortoise import Tortoise, run_async

from database.models import RawAddress
from helpers import db_connection


def convert_decimals(obj):
    """
    Рекурсивно преобразует все объекты Decimal в float.
    """
    if isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    if isinstance(obj, Decimal):
        return float(obj)
    return obj


def read_json_in_chunks(file_path: str, chunk_size: int = 1000):
    """
    Генератор, который считывает JSON-файл (в формате массива объектов)
    и возвращает данные порциями по chunk_size записей.
    """
    with open(file_path, "r", encoding="cp1251") as f:
        data = json.load(f)  # Загружаем весь файл
        for i in range(0, len(data), chunk_size):
            yield data[i : i + chunk_size]


async def load_raw_addresses(file_path: str):
    """
    Загружает данные из JSON-файла в таблицу RawAddress.
    """
    async with Tortoise.get_connection("default")._in_transaction():
        # Загружаем все существующие global_id из базы данных
        existing_ids = set(
            record.get("global_id")
            for record in await RawAddress.all().values_list("raw_data", flat=True)
            if record.get("global_id") is not None
        )

        total_count = 0
        async for chunk in async_iter(read_json_in_chunks(file_path)):
            # Преобразуем каждую запись (например, заменяя Decimal на float)
            records = [convert_decimals(record) for record in chunk]

            # Фильтруем записи: оставляем только те, которых нет в базе
            new_records = [
                RawAddress(raw_data=record)
                for record in records
                if record.get("global_id") is None
                or record.get("global_id") not in existing_ids
            ]

            if new_records:
                await RawAddress.bulk_create(new_records)
                total_count += len(new_records)
                print(f"Добавлено записей: {len(new_records)}, Всего: {total_count}")


async def async_iter(generator):
    """
    Преобразует синхронный генератор в асинхронный.
    """
    for item in generator:
        yield item
        await asyncio.sleep(0)  # Позволяет переключаться между задачами


async def main():
    """
    Основная функция для инициализации базы данных и загрузки данных.
    """
    async with db_connection():
        # Укажите путь к вашему JSON-файлу с данными
        file_path = "src/json/data-60562-2025-04-04.json"
        await load_raw_addresses(file_path)


if __name__ == "__main__":
    run_async(main())
