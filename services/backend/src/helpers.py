from contextlib import asynccontextmanager
from tortoise import Tortoise
import os

@asynccontextmanager
async def db_connection():
    """
    Контекстный менеджер для управления соединением с базой данных.
    """
    config = {
        "connections": {
            "default": os.environ.get("DATABASE_URL", "postgres://hello_fastapi:hello_fastapi@localhost:5432/hello_fastapi_dev")
        },
        "apps": {
            "models": {
                "models": ["src.database.models", "aerich.models"],  # Укажите полный путь к моделям
                "default_connection": "default",
            }
        },
    }
    
    await Tortoise.init(config=config)
    await Tortoise.generate_schemas()
    
    try:
        yield Tortoise
    finally:
        await Tortoise.close_connections()
