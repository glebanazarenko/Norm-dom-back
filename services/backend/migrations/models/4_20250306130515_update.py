from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "houses" ALTER COLUMN "obj_type" DROP NOT NULL;
        ALTER TABLE "houses" ALTER COLUMN "kad_n" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "houses" ALTER COLUMN "obj_type" SET NOT NULL;
        ALTER TABLE "houses" ALTER COLUMN "kad_n" SET NOT NULL;"""
