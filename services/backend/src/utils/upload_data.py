import asyncio
import json
from decimal import Decimal
from pathlib import Path

from tortoise import Tortoise, run_async

from src.database.models import RawAddress
from src.helpers import db_connection
from src.main import logger


def convert_decimals(obj):
    """
    Рекурсивно преобразует все объекты Decimal в float.
    """
    if isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj


def read_json_in_chunks(file_path: str, chunk_size: int = 1000):
    """
    Генератор, который считывает JSON-файл (в формате массива объектов)
    и возвращает данные порциями по chunk_size записей.
    """
    logger.info("Начинаю обработку файла")
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
                logger.info(
                    f"Добавлено записей: {len(new_records)}, Всего: {total_count}"
                )
            else:
                logger.info("Нет новых данных для вставки в chunck")


async def async_iter(generator):
    """
    Преобразует синхронный генератор в асинхронный.
    """
    for item in generator:
        yield item
        await asyncio.sleep(0)  # Позволяет переключаться между задачами


def get_latest_json_file() -> str | None:
    """
    Finds the most recently modified JSON file in the 'src/json/' directory.
    Returns the full path of the latest file or None if no files exist.
    """
    # Define the target directory (adjust based on script location)
    directory = Path(__file__).parent.parent / "json"

    if not directory.exists():
        logger.warning(f"Directory {directory} does not exist.")
        return None

    # Get all JSON files in the directory
    files = list(directory.glob("*.json"))
    if not files:
        logger.warning(f"No JSON files found in {directory}.")
        return None

    # Sort files by modification time (newest first)
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return str(files[0])


async def main():
    """
    Основная функция для инициализации базы данных и загрузки данных.
    """
    logger.info(f"Начинаю загружать данные в бд")
    async with db_connection():
        file_path = get_latest_json_file()
        logger.info(file_path)
        await load_raw_addresses(file_path)


if __name__ == "__main__":
    run_async(main())
