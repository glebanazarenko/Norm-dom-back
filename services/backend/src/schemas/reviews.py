from tortoise.contrib.pydantic import pydantic_model_creator
from src.database.models import House
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class EditReviewSchema(BaseModel):
    review_id: UUID
    new_rating: int
    new_review_text: str

class ModerateReviewSchema(BaseModel):
    review_id: UUID
    action: str  # "approve" или "reject"

class ReviewOutSchema(BaseModel):
    id: UUID
    house_id: UUID
    user_id: UUID
    rating: int
    review_text: str
    is_published: bool
    is_deleted: bool
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True