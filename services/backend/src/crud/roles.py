from src.database.models import Role

async def get_role(role_name: str):
    return await Role.get(role_name=role_name)