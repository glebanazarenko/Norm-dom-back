from tortoise import BaseDBAsyncClient

async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "adm_areas" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "name" VARCHAR(255) NOT NULL UNIQUE
        );
        COMMENT ON TABLE "adm_areas" IS 'Справочник административных округов.';

        CREATE TABLE IF NOT EXISTS "districts" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "name" VARCHAR(255) NOT NULL UNIQUE
        );
        COMMENT ON TABLE "districts" IS 'Справочник муниципальных округов/поселений.';

        CREATE TABLE IF NOT EXISTS "houses" (
            "id" SERIAL NOT NULL PRIMARY KEY,
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
            "adm_area_id" INT NOT NULL REFERENCES "adm_areas" ("id") ON DELETE CASCADE,
            "district_id" INT NOT NULL REFERENCES "districts" ("id") ON DELETE CASCADE
        );
        COMMENT ON TABLE "houses" IS 'Основная таблица объектов недвижимости.';

        CREATE TABLE IF NOT EXISTS "raw_addresses" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "raw_data" JSONB NOT NULL
        );
        COMMENT ON TABLE "raw_addresses" IS 'Таблица для сырого хранения загруженных CSV-данных.';

        CREATE TABLE IF NOT EXISTS "roles" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "role_name" VARCHAR(50) NOT NULL UNIQUE
        );
        COMMENT ON TABLE "roles" IS 'Справочник ролей пользователей.';

        CREATE TABLE IF NOT EXISTS "users" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "username" VARCHAR(20) NOT NULL UNIQUE,
            "full_name" VARCHAR(50),
            "email" VARCHAR(255) NOT NULL UNIQUE,
            "password" VARCHAR(128),
            "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "role_id" INT NOT NULL REFERENCES "roles" ("id") ON DELETE CASCADE
        );
        COMMENT ON TABLE "users" IS 'Таблица пользователей. Каждый пользователь имеет одну роль.';

        CREATE TABLE IF NOT EXISTS "reviews" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "rating" INT NOT NULL,
            "review_text" TEXT NOT NULL,
            "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "house_id" INT NOT NULL REFERENCES "houses" ("id") ON DELETE CASCADE,
            "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
        );
        COMMENT ON TABLE "reviews" IS 'Отзывы пользователей к объектам недвижимости.';

        CREATE TABLE IF NOT EXISTS "aerich" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "version" VARCHAR(255) NOT NULL,
            "app" VARCHAR(100) NOT NULL,
            "content" JSONB NOT NULL
        );

        -- Добавление ролей
        INSERT INTO "roles" ("role_name") VALUES 
            ('Admin'), 
            ('Super User'), 
            ('User')
        ON CONFLICT DO NOTHING;
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "reviews";
        DROP TABLE IF EXISTS "users";
        DROP TABLE IF EXISTS "roles";
        DROP TABLE IF EXISTS "raw_addresses";
        DROP TABLE IF EXISTS "houses";
        DROP TABLE IF EXISTS "districts";
        DROP TABLE IF EXISTS "adm_areas";
        DROP TABLE IF EXISTS "aerich";
    """
