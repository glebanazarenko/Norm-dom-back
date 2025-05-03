import pytest_asyncio
from tortoise import Tortoise
import httpx

from src.main import app
from src.database.models import User, Role, House, Review, AdmArea, District
from src.crud.users import pwd_context
from src.schemas.users import UserOutSchema
from src.auth.jwthandler import get_current_user


TORTOISE_ORM = {
    "connections": {"default": "sqlite://:memory:"},  # Используйте SQLite в памяти для тестов
    "apps": {
        "models": {
            "models": ["src.database.models", "aerich.models"],  # Укажите пути к моделям
            "default_connection": "default",
        }
    },
}

@pytest_asyncio.fixture(autouse=True)
async def initialize_tests():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["src.database.models", "aerich.models"]}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def user(role_user):
    encrypt_password = pwd_context.hash("password_user")
    user = await User.create(username="User", email="User@example.com", password=encrypt_password, role=role_user)
    return user

@pytest_asyncio.fixture
async def another_user(role_user):
    encrypt_password = pwd_context.hash("password_user")
    obj = await User.create(
        username="anotheruser",
        full_name="Another User",
        email="another@example.com",
        password=encrypt_password,
        role=role_user
    )
    return obj

@pytest_asyncio.fixture
async def role_user():
    return await Role.create(role_name="User")


@pytest_asyncio.fixture
async def superuser():
    role = await Role.create(role_name="Super User")
    encrypt_password = pwd_context.hash("password_superuser")
    # encrypt_password = pwd_context.hash("password_superuser")
    user = await User.create(username="superuser", email="superuser@example.com", password=encrypt_password, role=role)
    return user  # Ensure the coroutine is awaited and the result is returned


@pytest_asyncio.fixture
async def admin():
    role = await Role.create(role_name="Admin")
    encrypt_password = pwd_context.hash("password_admin")
    user = await User.create(username="admin", email="admin@example.com", password=encrypt_password, role=role)
    return user


@pytest_asyncio.fixture
async def adm_area():
    return await AdmArea.create(name="Test Adm Area")  # Используйте актуальные поля


@pytest_asyncio.fixture
async def district(adm_area):
    return await District.create(name="Test District", adm_area=adm_area)  # Пример связи


@pytest_asyncio.fixture
async def house(adm_area, district):
    house_instance = await House.create(
        unom="test_house",
        full_address="Test Address",
        simple_address="Test Simple Address",
        adm_area=adm_area,  # Указываем связанный AdmArea
        district=district   # Указываем связанный District
    )
    return house_instance

@pytest_asyncio.fixture
async def multiple_houses(house, adm_area, district):
    house2 = await House.create(
        unom="another_house",
        full_address="Another Address",
        simple_address="Another Simple Address",
        adm_area=adm_area,
        district=district
    )
    return [house, house2]

@pytest_asyncio.fixture
async def review(house, user):
    return await Review.create(
        house=house,
        user=user,
        rating=4,
        review_text="Отличный дом!",
        is_published=False,
        is_deleted=False
    )

@pytest_asyncio.fixture
async def review_superuser(house, superuser):
    return await Review.create(
        house=house,
        user=superuser,
        rating=4,
        review_text="Отличный дом!",
        is_published=False,
        is_deleted=False
    )


@pytest_asyncio.fixture
async def mock_authenticated_user(user):
    async def override_get_current_user():
        return await UserOutSchema.from_queryset_single(
            User.get(username=user.username)
        )

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield override_get_current_user
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def mock_authenticated_superuser(superuser):
    async def override_get_current_user():
        return await UserOutSchema.from_queryset_single(
            User.get(username=superuser.username)
        )

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield override_get_current_user
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def mock_authenticated_admin(admin):
    async def override_get_current_user():
        return await UserOutSchema.from_queryset_single(
            User.get(username=admin.username)
        )

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield override_get_current_user
    app.dependency_overrides.clear()
