import os
import shutil

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist
from tortoise.queryset import QuerySet

import src.utils.download_data as download
import src.utils.update_houses as update
import src.utils.upload_data as upload
from src.auth.jwthandler import get_current_user
from src.database.models import House, Review, Role, User
from src.schemas.reviews import (
    ModerateReviewSchema,
    PendingReviewSchema,
    ReviewOutSchema,
)
from src.schemas.roles import ChangeRoleSchema
from src.schemas.users import UserOutAdminSchema, UserOutSchema
from src.services.reviews import moderate_review
from src.services.users import is_admin

router = APIRouter()


@router.post("/admin/download")
async def download_data(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    await is_admin(current_user)

    # Define target directory
    target_dir = "src/json/"
    os.makedirs(target_dir, exist_ok=True)

    file_path = os.path.join(target_dir, file.filename)
    if os.path.exists(file_path):
        raise HTTPException(status_code=500, detail="Уже загружен этот файл в систему")

    try:
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": "Файл успешно загружен", "file_path": file_path}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при сохранении файла: {str(e)}"
        )


@router.post("/admin/upload")
async def upload_data(current_user: UserOutSchema = Depends(get_current_user)):
    await is_admin(current_user)
    await upload.main()
    return JSONResponse(content={"message": "Upload completed"})


@router.post("/admin/update-houses")
async def update_houses(current_user: UserOutSchema = Depends(get_current_user)):
    await is_admin(current_user)
    await update.main()
    return JSONResponse(content={"message": "Update completed"})


@router.post("/review/moderate", response_model=ReviewOutSchema)
async def moderate_review_route(
    data: ModerateReviewSchema, current_user: UserOutSchema = Depends(get_current_user)
):
    await is_admin(current_user)
    try:
        return await moderate_review(data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/admin/stats")
async def get_admin_stats(current_user: UserOutSchema = Depends(get_current_user)):
    await is_admin(current_user)
    try:
        # 1. Последнее обновление данных
        latest_house = await House.all().order_by("-updated_at").first()
        latest_time = None
        if latest_house:
            latest_time = latest_house.updated_at

        # 2. Количество домов
        total_houses = await House.all().count()

        # 3. Количество пользователей
        total_users = await User.all().count()

        # 4. Всего отзывов
        total_reviews = await Review.all().count()

        # 5. Отзывов на модерации (не опубликованные и не удалённые)
        pending_reviews = await Review.filter(
            is_published=False, is_deleted=False
        ).count()

        # 6. Средний рейтинг
        published_reviews = await Review.filter(
            is_deleted=False, is_published=True
        ).all()
        avg_rating = 0
        total = 0
        if published_reviews:
            total = sum(review.rating for review in published_reviews)
            avg_rating = total / len(published_reviews)

        return {
            "last_house_update": latest_time,
            "total_houses": total_houses,
            "total_users": total_users,
            "total_reviews": total_reviews,
            "pending_reviews": pending_reviews,
            "average_rating": round(avg_rating, 2) if avg_rating else 0,
        }
    except HTTPException as e:
        raise e


@router.get("/admin/pending-reviews", response_model=list[PendingReviewSchema])
async def get_pending_reviews(current_user: dict = Depends(get_current_user)):
    await is_admin(current_user)

    # Fetch all unapproved and non-deleted reviews
    # and include related user and house data
    reviews: QuerySet[Review] = Review.filter(
        is_published=False, is_deleted=False
    ).prefetch_related("user", "house")

    result = []
    async for review in reviews:
        result.append(
            PendingReviewSchema(
                id=str(review.id),
                house_id=str(review.house_id),
                house_address=review.house.simple_address,
                user_id=str(review.user_id),
                username=review.user.full_name or "Пользователь",
                rating=review.rating,
                review_text=review.review_text,
                created_at=review.created_at,
                modified_at=review.modified_at,
            )
        )

    return result


@router.get("/admin/users", response_model=list[UserOutAdminSchema])
async def get_users(
    current_user: dict = Depends(get_current_user),
    role: str
    | None = Query(None, description="Filter by role (Admin, Super User, User)"),
    is_blocked: bool | None = Query(None, description="Filter by block status"),
):
    await is_admin(current_user)

    # Base query
    users: QuerySet[User] = User.all().prefetch_related("role")

    # Apply filters
    if role:
        users = users.filter(role__role_name=role)

    if is_blocked is not None:
        users = users.filter(is_blocked=is_blocked)

    result = []
    async for user in users:
        total_reviews = await Review.filter(user=user).all().count()

        result.append(
            UserOutAdminSchema(
                id=str(user.id),
                username=user.username,
                full_name=user.full_name or "Не указано",
                email=user.email,
                role_name=user.role.role_name,
                created_at=user.created_at,
                is_blocked=user.is_blocked,
                reviews_count=total_reviews,
            )
        )

    return result


@router.post("/admin/users/{user_id}/block")
async def block_user(
    user_id: str,
    current_user: dict = Depends(get_current_user),
):
    await is_admin(current_user)

    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.is_blocked = True
    await user.save()
    return {"status": "blocked", "username": user.username}


@router.post("/admin/users/{user_id}/unblock")
async def unblock_user(
    user_id: str,
    current_user: dict = Depends(get_current_user),
):
    await is_admin(current_user)

    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.is_blocked = False
    await user.save()
    return {"status": "unblocked", "username": user.username}


@router.post("/admin/users/{user_id}/role", response_model=dict)
async def change_user_role(
    user_id: str,
    data: ChangeRoleSchema,
    current_user: dict = Depends(get_current_user),
):
    await is_admin(current_user)

    try:
        # Get the user by ID
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Get the target role
        role = await Role.get_or_none(role_name=data.role)
        if not role:
            raise HTTPException(status_code=400, detail="Недопустимая роль")

        # Update the user's role
        user.role = role
        await user.save()

        return {
            "status": "success",
            "message": f"Роль пользователя {user.username} изменена на {data.role}",
        }

    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Пользователь или роль не найдены")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при изменении роли: {str(e)}"
        )
