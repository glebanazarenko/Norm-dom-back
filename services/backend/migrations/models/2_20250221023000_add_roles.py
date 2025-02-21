from tortoise import BaseDBAsyncClient

async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
    INSERT INTO "roles" ("id", "role_name") VALUES 
        (gen_random_uuid(), 'Admin'), 
        (gen_random_uuid(), 'Super User'), 
        (gen_random_uuid(), 'User')
    ON CONFLICT (role_name) DO NOTHING;
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
    DELETE FROM "roles" WHERE role_name IN ('Admin', 'Super User', 'User');
    """
