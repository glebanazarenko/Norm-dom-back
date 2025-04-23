from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- Добавляем новое поле modified_at с автоматическим обновлением времени
        ALTER TABLE "reviews" ADD "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        
        -- Добавляем новое поле is_published с значением по умолчанию False
        ALTER TABLE "reviews" ADD "is_published" BOOL NOT NULL DEFAULT FALSE;
        
        -- Добавляем новое поле is_deleted с значением по умолчанию False
        ALTER TABLE "reviews" ADD "is_deleted" BOOL NOT NULL DEFAULT FALSE;
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- Удаляем поле modified_at
        ALTER TABLE "reviews" DROP COLUMN "modified_at";
        
        -- Удаляем поле is_published
        ALTER TABLE "reviews" DROP COLUMN "is_published";
        
        -- Удаляем поле is_deleted
        ALTER TABLE "reviews" DROP COLUMN "is_deleted";
    """