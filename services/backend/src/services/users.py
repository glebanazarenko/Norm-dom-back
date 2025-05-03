from uuid import UUID

from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.crud.roles import get_role
from src.crud.users import (
    create_user_in_db,
    delete_user_by_id,
    get,
    get_first_user,
    get_user,
)
from src.schemas.token import Status
from src.schemas.users import UserFrontSchema, UserInSchema, UserOutSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def is_admin(user: UserOutSchema):
    user_data = await get_user(user.username)
    if not user_data or user_data.role_name != "Admin":
        raise HTTPException(status_code=403, detail="Access denied: Admins only")
    return user_data


async def is_super_user(user: UserOutSchema):
    user_data = await get_user(user.username)
    if not user_data or user_data.role_name != "Super User":
        raise HTTPException(status_code=403, detail="Access denied: Super Users only")
    return user_data


async def create_user_with_logic(user: UserInSchema) -> UserOutSchema:
    user.password = pwd_context.hash(user.password)

    existing_user = await get_first_user(username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")

    user_dict = user.dict(exclude_unset=True)

    if "role_id" not in user_dict:
        default_role = await get_role(role_name="User")
        user_dict["role_id"] = default_role.id

    try:
        user_obj = await create_user_in_db(user_dict)
    except IntegrityError as err:
        raise HTTPException(status_code=400, detail=str(err))

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def get_user_with_logic(username: str) -> UserFrontSchema:
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=400, detail="Нет такого пользователя")
    return user


async def delete_user_with_logic(user_id: UUID, current_user_id: UUID) -> Status:
    try:
        await get(user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Пользователь {user_id} не найден")

    if user_id == current_user_id:
        deleted_count = await delete_user_by_id(user_id)
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")  # UPDATED

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
