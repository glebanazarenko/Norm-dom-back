import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from src.database.config import TORTOISE_ORM
from src.database.register import register_tortoise

# Глобальная настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



# enable schemas to read relationship between models
Tortoise.init_models(["src.database.models"], "models")

"""
import 'from src.routes import users, notes' must be after 'Tortoise.init_models'
why?
https://stackoverflow.com/questions/65531387/tortoise-orm-for-python-no-returns-relations-of-entities-pyndantic-fastapi
"""
from src.routes import admin, houses, super_user, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://127.0.0.1:8081", "http://localhost:5001", "http://127.0.0.1:5001"],
    allow_credentials=True,  # <-- Должно быть True, иначе `cookies` не работают
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, OPTIONS и т. д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(houses.router)
app.include_router(super_user.router)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get("/")
def home():
    return "Hello, World!"