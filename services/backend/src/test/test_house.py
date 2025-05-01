import pytest

@pytest.mark.asyncio
async def test_create_review_user(house, client, mock_authenticated_user):
    response = await client.post(
        f"/house/{house.id}/reviews",
        json={"review_data": "Great house!", "rating": 5},
        headers={ 'Content-Type': 'application/json' }
    )
    assert response.status_code == 200, f"Ошибка: {response.json()}"
    json_response = response.json()
    assert json_response["reviews"][0]["rating"] == 5
    assert json_response["reviews"][0]["is_published"] is False


@pytest.mark.asyncio
async def test_create_review_superuser(house, client, mock_authenticated_superuser):
    response = await client.post(
        f"/house/{house.id}/reviews",
        json={"review_data": "Great house!", "rating": 5},
        headers={ 'Content-Type': 'application/json' }
    )
    assert response.status_code == 200, f"Ошибка: {response.json()}"
    json_response = response.json()
    assert json_response["reviews"][0]["rating"] == 5
    assert json_response["reviews"][0]["is_published"] is False


@pytest.mark.asyncio
async def test_create_review_admin(house, client, mock_authenticated_admin):
    response = await client.post(
        f"/house/{house.id}/reviews",
        json={"review_data": "Great house!", "rating": 5},
        headers={ 'Content-Type': 'application/json' }
    )
    assert response.status_code == 200, f"Ошибка: {response.json()}"
    json_response = response.json()
    assert json_response["reviews"][0]["rating"] == 5
    assert json_response["reviews"][0]["is_published"] is False

@pytest.mark.asyncio
async def test_search_houses_found(house, client):
    response = await client.get("/houses/search?query=test_house")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["unom"] == house.unom
    assert data[0]["full_address"] == house.full_address
    assert data[0]["simple_address"] == house.simple_address
    assert data[0]["adm_area"]['name'] == house.adm_area.name
    assert data[0]["district"]['name'] == house.district.name

@pytest.mark.asyncio
async def test_search_houses_multiple(multiple_houses, client):
    response = await client.get("/houses/search?query=test")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # Проверьте, что query "test" соответствует только первому дому

    response = await client.get("/houses/search?query=another")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["unom"] == "another_house"

@pytest.mark.asyncio
async def test_search_houses_not_found(client):
    response = await client.get("/houses/search?query=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Нет такого дома"}

@pytest.mark.asyncio
async def test_search_houses_empty_query(client):
    response = await client.get("/houses/search?query=")
    assert response.status_code == 404
    assert response.json() == {"detail": "Дом не найден"}

@pytest.mark.asyncio
async def test_search_houses_no_query(client):
    response = await client.get("/houses/search")
    assert response.status_code == 422  # FastAPI возвращает 422, если query не передан

@pytest.mark.asyncio
async def test_get_house_by_id_found(house, client):
    response = await client.get(f"/house/{house.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(house.id)

@pytest.mark.asyncio
async def test_get_house_by_id_not_found(client):
    response = await client.get("/house/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Нет такого дома"}

@pytest.mark.asyncio
async def test_get_house_by_id_invalid_uuid(client):
    response = await client.get("/house/invalid-uuid")
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_house_by_id_missing_house(house, client):
    # Создаем дом, но используем другой UUID
    non_existent_id = "123e4567-e89b-12d3-a456-426614174001"
    response = await client.get(f"/house/{non_existent_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Нет такого дома"}