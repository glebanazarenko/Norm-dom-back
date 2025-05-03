from uuid import uuid4

import jwt
import pytest

from src.auth.jwthandler import ALGORITHM, SECRET_KEY
from src.crud.users import delete_user_by_id, get, get_user, pwd_context
from src.database.models import User


@pytest.mark.asyncio
async def test_login(client, user, superuser, admin):
    # Вход в систему
    login_response = await client.post(
        "/login", data={"username": user.username, "password": "password_user"}
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
        data={"username": superuser.username, "password": "password_superuser"},
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
        "/login", data={"username": admin.username, "password": "password_admin"}
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
        "password": "SecurePass123!",
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
        "password": "SecurePass123!",
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


@pytest.mark.asyncio
async def test_delete_user_success(client, user, mock_authenticated_user):
    response = await client.delete(f"/user/{user.id}")
    assert response.status_code == 200, f"Ошибка: {response.json()}"
    data = response.json()
    assert data["message"] == f"Deleted user {str(user.id)}"


@pytest.mark.asyncio
async def test_delete_user_not_found(client, user, mock_authenticated_user):
    fake_id = uuid4()
    response = await client.delete(f"/user/{fake_id}")
    assert response.status_code == 404, f"Ошибка: {response.json()}"
    assert response.json()["detail"] == f"Пользователь {str(fake_id)} не найден"


@pytest.mark.asyncio
async def test_delete_user_unauthorized(client, another_user):
    response = await client.delete(f"/user/{another_user.id}")
    assert response.status_code == 401, f"Ошибка: {response.json()}"
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_delete_wrong_user(client, another_user, mock_authenticated_superuser):
    response = await client.delete(f"/user/{another_user.id}")
    assert response.status_code == 403, f"Ошибка: {response.json()}"
    assert response.json()["detail"] == "Not authorized to delete"


@pytest.mark.asyncio
async def test_get_user_found(user):
    result = await get_user(user.username)
    assert result.username == user.username


@pytest.mark.asyncio
async def test_get_user_by_id(user):
    result = await get(user.id)
    assert result.id == user.id
    assert result.username == user.username


@pytest.mark.asyncio
async def test_delete_user_by_id(user):
    count = await delete_user_by_id(user.id)
    assert count == 1
    result = await User.get_or_none(id=user.id)
    assert result is None
