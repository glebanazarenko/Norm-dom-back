import pytest
from src.database.models import User, Role, House, Review, AdmArea, District

@pytest.mark.asyncio
async def test_edit_review_success(review_superuser, client, superuser, mock_authenticated_superuser):
    # Проверка, что отзыв существует
    existing_review = await Review.get_or_none(id=review_superuser.id)
    assert existing_review is not None

    # Подготовка данных
    data = {
        "review_id": str(review_superuser.id),
        "new_rating": 5,
        "new_review_text": "Отличный дом после редактирования"
    }

    # Выполнение запроса
    response = await client.post("/review/edit", json=data)
    assert response.status_code == 200, f"Ошибка: {response.json()}"

    # Проверка результата
    json_response = response.json()
    assert json_response["rating"] == 5
    assert json_response["review_text"] == "Отличный дом после редактирования"
    assert json_response["modified_at"] != review_superuser.modified_at.isoformat()


@pytest.mark.asyncio
async def test_edit_review_unauthorized(review, client, mock_authenticated_admin):
    data = {
        "review_id": str(review.id),
        "new_rating": 5,
        "new_review_text": "Новый текст"
    }

    response = await client.post("/review/edit", json=data)
    assert response.status_code == 403, f"Ошибка: {response.json()}"
    assert response.json() == {"detail": "Access denied: Super Users only"}

@pytest.mark.asyncio
async def test_edit_review_unauthorized(review, client, mock_authenticated_user):
    data = {
        "review_id": str(review.id),
        "new_rating": 5,
        "new_review_text": "Новый текст"
    }

    response = await client.post("/review/edit", json=data)
    assert response.status_code == 403, f"Ошибка: {response.json()}"
    assert response.json() == {"detail": "Access denied: Super Users only"}

@pytest.mark.asyncio
async def test_edit_review_not_found(client, mock_authenticated_superuser):
    data = {
        "review_id": "123e4567-e89b-12d3-a456-426614174000",
        "new_rating": 5,
        "new_review_text": "Новый текст"
    }

    response = await client.post("/review/edit", json=data)
    assert response.status_code == 404, f"Ошибка: {response.json()}"
    assert response.json() == {"detail": "Отзыв не найден или не принадлежит вам"}

@pytest.mark.asyncio
async def test_edit_review_invalid_uuid(client, mock_authenticated_superuser):
    data = {
        "review_id": "invalid-uuid",
        "new_rating": 5,
        "new_review_text": "Новый текст"
    }

    response = await client.post("/review/edit", json=data)
    assert response.status_code == 422, f"Ошибка: {response.json()}"



