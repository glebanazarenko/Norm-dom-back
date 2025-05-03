from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import House

# Схема для входных данных (если потребуется создание дома)
HouseInSchema = pydantic_model_creator(
    House,
    name="HouseIn",
    exclude=("id", "created_at", "updated_at", "geo_data", "geodata_center"),
)

# Схема для вывода данных на фронтенд
HouseOutFrontSchema = pydantic_model_creator(
    House,
    name="HouseOutFront",
    exclude=(
        "geo_data",
        "geodata_center",
        "kad_n",
        "kad_zu",
        "created_at",
        "updated_at",
    ),
)

# Схема для полного представления дома (для админов)
HouseOutSchema = pydantic_model_creator(
    House,
    name="HouseOut",
    exclude=("geo_data", "geodata_center"),
)

# Схема для хранения данных в базе данных
HouseDatabaseSchema = pydantic_model_creator(
    House,
    name="HouseDatabase",
    exclude=("geo_data", "geodata_center"),
)


# Схема для создания отзыва
class ReviewCreateSchema(BaseModel):
    review_text: str
    rating: int

    class Config:
        schema_extra = {
            "example": {
                "review_text": "Отличный дом!",
                "rating": 5,
            }
        }


# class HouseFrontSchema(UserOutFrontSchema):
#     role_name: str

#     class Config:
#         orm_mode = True

#     @classmethod
#     def from_orm(cls, obj):
#         # Получаем связанные данные, включая role_name
#         obj.role_name = obj.role.role_name  # Добавляем поле role_name
#         return obj
