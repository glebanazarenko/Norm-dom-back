import pytest
import jwt

from src.crud.users import pwd_context
from src.database.models import User, Role, House, Review, AdmArea, District
from src.auth.jwthandler import SECRET_KEY, ALGORITHM

@pytest.mark.asyncio
async def test_login(client, user, superuser, admin):
    # Вход в систему
    login_response = await client.post(
        "/login",
        data={"username": user.username, "password": "password_user"}
    )
    assert login_response.status_code == 200, "Ошибка входа"    
    # Извлечение токена
    assert "Authorization" in login_response.cookies
    auth_cookie = login_response.cookies.get("Authorization")
    assert auth_cookie, "Куки Authorization не найдены"
    token = auth_cookie.split(" ")[1].strip('"')  # Удаляем кавычки в конце
    # Проверка токена
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == user.username, "Неверный sub в токене"

    # Вход в систему
    login_response = await client.post(
        "/login",
        data={"username": superuser.username, "password": "password_superuser"}
    )
    assert login_response.status_code == 200, "Ошибка входа"
    # Извлечение токена
    assert "Authorization" in login_response.cookies
    auth_cookie = login_response.cookies.get("Authorization")
    assert auth_cookie, "Куки Authorization не найдены"
    token = auth_cookie.split(" ")[1].strip('"')  # Удаляем кавычки в конце
    # Проверка токена
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == superuser.username, "Неверный sub в токене"

    # Вход в систему
    login_response = await client.post(
        "/login",
        data={"username": admin.username, "password": "password_admin"}
    )
    assert login_response.status_code == 200, "Ошибка входа"
    # Извлечение токена
    assert "Authorization" in login_response.cookies
    auth_cookie = login_response.cookies.get("Authorization")
    assert auth_cookie, "Куки Authorization не найдены"
    token = auth_cookie.split(" ")[1].strip('"')  # Удаляем кавычки в конце
    # Проверка токена
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == admin.username, "Неверный sub в токене"


@pytest.mark.asyncio
async def test_register_user_success(client, role_user):
    user_data = {
        "username": "new_user",
        "full_name": "New user",
        "email": "new@example.com",
        "password": "SecurePass123!"
    }
    response = await client.post("/register", json=user_data)
    assert response.status_code == 200, f"Ошибка: {response.json()}"
    data = response.json()
    assert data["username"] == user_data["username"]
    created_user = await User.get(username="new_user")
    assert pwd_context.verify(user_data["password"], created_user.password)


@pytest.mark.asyncio
async def test_register_existing_email(client, user):
    user_data = {
        "username": "existing_user",
        "full_name": "Exist user",
        "email": user.email,
        "password": "SecurePass123!"
    }
    response = await client.post("/register", json=user_data)
    assert response.status_code == 400, f"Ошибка: {response.json()}"


@pytest.mark.asyncio
async def test_register_existing_username(client, user):
    user_data = {
        "username": user.username,
        "full_name": "Exist user",
        "email": "another@example.com",
        "password": "SecurePass123!",
    }
    response = await client.post("/register", json=user_data)
    assert response.status_code == 400, f"Ошибка: {response.json()}"



# @pytest.mark.asyncio
# async def test_admin_cannot_edit_review(superuser, admin, house, client):
#     # Создаем отзыв под суперпользователем
#     review = await Review.create(house=house, user=superuser, rating=4, review_text="Nice house!")

#     # Пытаемся изменить отзыв под админом
#     admin_token = create_access_token({"sub": "admin"})
#     headers = {"Authorization": f"Bearer {admin_token}"}

#     response = client.post(
#         "/review/edit",
#         json={"review_id": str(review.id), "new_rating": 3, "new_review_text": "Not so nice"},
#         headers=headers
#     )
#     assert response.status_code == 403  # Доступ запрещен

# @pytest.mark.asyncio
# async def test_admin_approve_review(superuser, admin, house, client):
#     # Создаем отзыв под суперпользователем
#     review = await Review.create(house=house, user=superuser, rating=4, review_text="Nice house!")

#     # Одобряем отзыв под админом
#     admin_token = create_access_token({"sub": "admin"})
#     headers = {"Authorization": f"Bearer {admin_token}"}

#     response = client.post(
#         "/review/moderate",
#         json={"review_id": str(review.id), "action": "approve"},
#         headers=headers
#     )
#     assert response.status_code == 200

#     # Проверяем, что отзыв опубликован
#     updated_review = await Review.get(id=review.id)
#     assert updated_review.is_published


# @pytest.mark.asyncio
# async def test_superuser_edit_approved_review(superuser, admin, house, client):
#     # Создаем отзыв под суперпользователем
#     review = await Review.create(house=house, user=superuser, rating=4, review_text="Nice house!")

#     # Одобряем отзыв под админом
#     admin_token = create_access_token({"sub": "admin"})
#     headers = {"Authorization": f"Bearer {admin_token}"}

#     response = client.post(
#         "/review/moderate",
#         json={"review_id": str(review.id), "action": "approve"},
#         headers=headers
#     )
#     assert response.status_code == 200

#     # Пытаемся изменить отзыв под суперпользователем
#     superuser_token = create_access_token({"sub": "superuser"})
#     headers = {"Authorization": f"Bearer {superuser_token}"}

#     response = client.post(
#         "/review/edit",
#         json={"review_id": str(review.id), "new_rating": 3, "new_review_text": "Updated review"},
#         headers=headers
#     )
#     assert response.status_code == 400  # Нельзя изменять опубликованный отзыв

# @pytest.mark.asyncio
# async def test_admin_delete_review(superuser, admin, house, client):
#     # Создаем отзыв под суперпользователем
#     review = await Review.create(house=house, user=superuser, rating=4, review_text="Nice house!")

#     # Удаляем отзыв под админом
#     admin_token = create_access_token({"sub": "admin"})
#     headers = {"Authorization": f"Bearer {admin_token}"}

#     response = client.delete(
#         f"/review/{review.id}",
#         headers=headers
#     )
#     assert response.status_code == 200

#     # Проверяем, что отзыв удален
#     deleted_review = await Review.get_or_none(id=review.id)
#     assert deleted_review.is_deleted