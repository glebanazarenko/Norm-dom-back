from shapely.geometry import shape
from tortoise import run_async

from src.database.models import AdmArea, District, House, RawAddress
from src.helpers import db_connection
from src.main import logger


async def migrate_data():
    async with db_connection():
        try:
            # Получаем все сырые адреса
            raw_addresses = await RawAddress.all()
            total = len(raw_addresses)
            logger.info(f"Начинаю миграцию {total} записей")

            # Собираем все существующие UNOM из БД
            existing_unoms_db = set(
                str(unom) for unom in await House.all().values_list("unom", flat=True)
            )
            logger.info(f"Найдено {len(existing_unoms_db)} существующих UNOM в БД")

            # Собираем уникальные административные округа и районы
            adm_area_names = set()
            district_names = set()

            for raw in raw_addresses:
                data = raw.raw_data
                if "ADM_AREA" in data:
                    adm_area_names.add(data["ADM_AREA"])
                if "DISTRICT" in data:
                    district_names.add(data["DISTRICT"])

            # Создаем административные округа
            existing_areas = set(
                await AdmArea.filter(name__in=adm_area_names).values_list(
                    "name", flat=True
                )
            )
            new_areas = adm_area_names - existing_areas
            if new_areas:
                await AdmArea.bulk_create([AdmArea(name=name) for name in new_areas])
            adm_areas = {a.name: a for a in await AdmArea.all()}

            # Создаем районы
            existing_districts = set(
                await District.filter(name__in=district_names).values_list(
                    "name", flat=True
                )
            )
            new_districts = district_names - existing_districts
            if new_districts:
                await District.bulk_create(
                    [District(name=name) for name in new_districts]
                )
            districts = {d.name: d for d in await District.all()}

            # Фильтруем и обрабатываем данные
            houses_to_create = []
            processed_unoms = set()

            for i, raw in enumerate(raw_addresses, 1):
                data = raw.raw_data
                raw_unom = data.get("UNOM")

                # Явное преобразование в строку
                unom = str(raw_unom) if raw_unom is not None else None

                # Пропускаем некорректные записи
                if not all([unom, data.get("ADM_AREA"), data.get("DISTRICT")]):
                    continue

                # Проверка уникальности
                if unom in existing_unoms_db or unom in processed_unoms:
                    continue

                try:
                    # Геоданные
                    geo_data = data.get("geoData")
                    geo_center = data.get("geodata_center")
                    geo_data_wkt = shape(geo_data).wkt if geo_data else None
                    geodata_center_wkt = shape(geo_center).wkt if geo_center else None

                    # Кадастровые номера
                    kad_n = data["KAD_N"][0]["KAD_N"] if data.get("KAD_N") else None
                    kad_zu = data["KAD_ZU"][0]["KAD_ZU"] if data.get("KAD_ZU") else None

                    # Создаем объект дома
                    house = House(
                        unom=unom,
                        obj_type=data.get("OBJ_TYPE", ""),
                        full_address=data.get("ADDRESS", ""),
                        simple_address=data.get("SIMPLE_ADDRESS", ""),
                        adm_area=adm_areas[data["ADM_AREA"]],
                        district=districts[data["DISTRICT"]],
                        kad_n=kad_n,
                        kad_zu=kad_zu,
                        geo_data=geo_data_wkt,
                        geodata_center=geodata_center_wkt,
                    )

                    houses_to_create.append(house)
                    processed_unoms.add(unom)

                    if i % 1000 == 0:
                        logger.info(f"Обработано {i} записей")

                except Exception as e:
                    logger.error(f"Ошибка обработки UNOM {unom}: {str(e)}")
                    continue

            # Вставка данных
            if houses_to_create:
                try:
                    await House.bulk_create(houses_to_create)
                    logger.info(f"УСПЕХ: Добавлено {len(houses_to_create)} домов")
                except Exception as e:
                    logger.error(f"Ошибка массовой вставки: {str(e)}")
            else:
                logger.info("Нет новых данных для вставки")

        except Exception as e:
            logger.error(f"Критическая ошибка: {str(e)}")
            raise


async def main():
    """
    Основная функция для инициализации базы данных и загрузки данных.
    """
    await migrate_data()


if __name__ == "__main__":
    run_async(main())
