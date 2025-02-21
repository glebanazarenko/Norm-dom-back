from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "adm_areas" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "districts" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "houses" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "unom" VARCHAR(255) NOT NULL UNIQUE,
    "obj_type" VARCHAR(100) NOT NULL,
    "full_address" TEXT NOT NULL,
    "simple_address" TEXT NOT NULL,
    "kad_n" TEXT NOT NULL,
    "kad_zu" TEXT,
    "geo_data" TEXT,
    "geodata_center" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "adm_area_id" UUID NOT NULL REFERENCES "adm_areas" ("id") ON DELETE CASCADE,
    "district_id" UUID NOT NULL REFERENCES "districts" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "raw_addresses" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "raw_data" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "roles" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "role_name" VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "full_name" VARCHAR(50),
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(128),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "role_id" UUID NOT NULL REFERENCES "roles" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "reviews" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "rating" INT NOT NULL,
    "review_text" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "house_id" UUID NOT NULL REFERENCES "houses" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
