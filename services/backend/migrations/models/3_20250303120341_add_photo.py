from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
CREATE TABLE IF NOT EXISTS "photos" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "base64_data" TEXT NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "metadata" JSONB,
    "house_id" UUID REFERENCES "houses" ("id") ON DELETE CASCADE,
    "review_id" UUID REFERENCES "reviews" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_settings" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "bio" TEXT,
    "preferences" JSONB,
    "profile_photo_id" UUID REFERENCES "photos" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL UNIQUE REFERENCES "users" ("id") ON DELETE CASCADE
);
"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
    DROP TABLE IF EXISTS "user_settings";
    DROP TABLE IF EXISTS "photos";
    """
