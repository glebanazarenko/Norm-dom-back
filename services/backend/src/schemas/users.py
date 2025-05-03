from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import User

UserInSchema = pydantic_model_creator(
    User,
    name="UserIn",
    include=("username", "full_name", "email", "password"),
)
UserOutSchema = pydantic_model_creator(
    User,
    name="UserOut",
    exclude=["password", "created_at", "modified_at", "email", "role"],
)
UserDatabaseSchema = pydantic_model_creator(
    User, name="User", exclude=["created_at", "modified_at"]
)
UserOutFrontSchema = pydantic_model_creator(
    User,
    name="UserOutFront",
    include=("username", "full_name", "email", "created_at", "modified_at"),
)


class UserFrontSchema(UserOutFrontSchema):
    role_name: str

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        # Получаем связанные данные, включая role_name
        obj.role_name = obj.role.role_name  # Добавляем поле role_name
        return obj
