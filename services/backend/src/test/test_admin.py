import pytest


@pytest.mark.asyncio
async def test_moderate_review_approve_success(
    review, client, mock_authenticated_admin
):
    # Подготовка данных
    data = {"review_id": str(review.id), "action": "approve"}

    # Выполнение запроса
    response = await client.post("/review/moderate", json=data)
    assert response.status_code == 200, f"Ошибка: {response.json()}"

    # Проверка результата
    json_response = response.json()
    assert json_response["is_published"] is True
    assert json_response["is_deleted"] is False


@pytest.mark.asyncio
async def test_moderate_review_reject_success(review, client, mock_authenticated_admin):
    data = {"review_id": str(review.id), "action": "reject"}

    response = await client.post("/review/moderate", json=data)
    assert response.status_code == 200, f"Ошибка: {response.json()}"

    json_response = response.json()
    assert json_response["is_published"] is False
    assert json_response["is_deleted"] is True


@pytest.mark.asyncio
async def test_moderate_review_invalid_action(review, client, mock_authenticated_admin):
    data = {"review_id": str(review.id), "action": "delete"}

    response = await client.post("/review/moderate", json=data)
    assert response.status_code == 400, f"Ошибка: {response.json()}"
    assert response.json() == {"detail": "Недопустимое действие"}


@pytest.mark.asyncio
async def test_moderate_review_not_found(client, mock_authenticated_admin):
    data = {"review_id": "123e4567-e89b-12d3-a456-426614174000", "action": "approve"}

    response = await client.post("/review/moderate", json=data)
    assert response.status_code == 404, f"Ошибка: {response.json()}"
    assert response.json() == {"detail": "Отзыв не найден"}


@pytest.mark.asyncio
async def test_moderate_review_unauthorized(review, client, mock_authenticated_user):
    data = {"review_id": str(review.id), "action": "approve"}

    response = await client.post("/review/moderate", json=data)
    assert response.status_code == 403, f"Ошибка: {response.json()}"
    assert response.json() == {"detail": "Access denied: Admins only"}


@pytest.mark.asyncio
async def test_moderate_review_unauthorized(
    review, client, mock_authenticated_superuser
):
    data = {"review_id": str(review.id), "action": "approve"}

    response = await client.post("/review/moderate", json=data)
    assert response.status_code == 403, f"Ошибка: {response.json()}"
    assert response.json() == {"detail": "Access denied: Admins only"}
