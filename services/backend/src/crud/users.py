from uuid import UUID

from fastapi import HTTPException
from passlib.context import CryptContext

from src.database.models import User
from src.schemas.users import UserFrontSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(username) -> UserFrontSchema:
    user_data = await User.filter(username=username).select_related("role").first()
    if user_data:
        # Создаем схему с использованием from_tortoise_orm для правильной сериализации
        return await UserFrontSchema.from_tortoise_orm(
            UserFrontSchema.from_orm(user_data)
        )
    # Возвращаем ошибку, если пользователь не найден
    raise HTTPException(status_code=400, detail="Нет такого пользователя")


async def get(id: UUID):
    return await User.get(id=id)

async def get_or_none(id: UUID):
    return await User.get_or_none(id=id)

async def get_first_user(username: str):
    return await User.filter(username=username).first()


async def create_user_in_db(data: dict):
    return await User.create(**data)


async def delete_user_by_id(user_id: UUID) -> int:
    return await User.filter(id=user_id).delete()
