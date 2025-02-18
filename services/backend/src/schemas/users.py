from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import User


UserInSchema = pydantic_model_creator(
    User, name="UserIn", include=("username", "full_name", 'email', "password"),
)
UserOutSchema = pydantic_model_creator(
    User, name="UserOut", exclude=["password", "created_at", "modified_at", 'email', 'role']
)
UserDatabaseSchema = pydantic_model_creator(
    User, name="User", exclude=["created_at", "modified_at"]
)