from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError
import logging


from src.database.models import User, Role
from src.schemas.token import Status  # NEW
from src.schemas.users import UserOutSchema, UserFrontSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def get_user(username) -> UserFrontSchema:
    user_data = await User.filter(username=username).select_related('role').first()

    if user_data:
        # Создаем схему с использованием from_tortoise_orm для правильной сериализации
        return await UserFrontSchema.from_tortoise_orm(UserFrontSchema.from_orm(user_data))
    
    # Возвращаем ошибку, если пользователь не найден
    raise HTTPException(status_code=400, detail="Нет такого пользователя")


async def create_user(user) -> UserOutSchema:
    logger.info(f"Начало создания пользователя: {user.username}")
    user.password = pwd_context.encrypt(user.password)

    # Проверяем, существует ли уже такой пользователь
    existing_user = await User.filter(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    
    user_dict = user.dict(exclude_unset=True)

    if "role_id" not in user_dict:
        default_role = await Role.get(role_name='User')  # Получаем объект роли
        user_dict["role_id"] = default_role.id  # Передаем `id`, а не объект

    logger.info(f'User data: {user_dict}')
    try:
        user_obj = await User.create(
            username=user_dict["username"],
            full_name=user_dict.get("full_name"),
            email=user_dict["email"],
            password=user_dict["password"],
            role_id=user_dict["role_id"],
        )
    except IntegrityError as err:
        logger.error(f"Ошибка создания пользователя: {err}")
        raise HTTPException(status_code=400, detail=str(err))

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def delete_user(user_id, current_user) -> Status:  # UPDATED
    logger.info(f"Начало удаления пользователя: {current_user.username}")
    try:
        db_user = await UserOutSchema.from_queryset_single(User.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    logger.info(f'User data: {db_user}')
    logger.info(f'User current: {current_user}')
    if db_user.id == current_user.id:
        deleted_count = await User.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")  # UPDATED

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")