import asyncio
from database.models import RawAddress, AdmArea, District, House
from shapely.geometry import shape
from helpers import db_connection

async def migrate_data():
    async with db_connection():
        raw_addresses = await RawAddress.all()
        total = len(raw_addresses)
        print(f"Начинаю миграцию {total} записей")

        # Предварительная обработка данных
        adm_area_names = set()
        district_names = set()
        unoms = []
        
        for raw in raw_addresses:
            data = raw.raw_data
            adm_area_names.add(data.get('ADM_AREA'))
            district_names.add(data.get('DISTRICT'))
            unoms.append(data.get('UNOM'))

        # Массовое создание административных округов
        existing_areas = await AdmArea.filter(name__in=adm_area_names).values_list('name', flat=True)
        new_areas = adm_area_names - set(existing_areas)
        await AdmArea.bulk_create([AdmArea(name=name) for name in new_areas])
        adm_areas = {area.name: area for area in await AdmArea.all()}

        # Массовое создание районов
        existing_districts = await District.filter(name__in=district_names).values_list('name', flat=True)
        new_districts = district_names - set(existing_districts)
        await District.bulk_create([District(name=name) for name in new_districts])
        districts = {d.name: d for d in await District.all()}

        # Фильтрация существующих UNOM
        existing_unoms = set(await House.filter(unom__in=unoms).values_list('unom', flat=True))
        filtered = [raw for raw in raw_addresses if raw.raw_data.get('UNOM') not in existing_unoms]

        print(f"Обнаружено {len(filtered)} новых записей для обработки")

        # Массовая обработка геоданных
        houses_to_create = []
        for i, raw in enumerate(filtered, 1):
            data = raw.raw_data

            # Пропуск неполных данных
            if not data.get('ADM_AREA') or not data.get('DISTRICT'):
                continue

            # Конвертация GeoJSON в WKT
            geo_data_wkt = shape(data['geoData']).wkt if data.get('geoData') else None
            geodata_center_wkt = shape(data['geodata_center']).wkt if data.get('geodata_center') else None

            # Обработка кадастровых номеров
            kad_n = data['KAD_N'][0]['KAD_N'] if data.get('KAD_N') else None
            kad_zu = data['KAD_ZU'][0]['KAD_ZU'] if data.get('KAD_ZU') else None

            house = House(
                unom=data['UNOM'],
                obj_type=data.get('OBJ_TYPE', ''),
                full_address=data.get('ADDRESS', ''),
                simple_address=data.get('SIMPLE_ADDRESS', ''),
                adm_area=adm_areas[data['ADM_AREA']],
                district=districts[data['DISTRICT']],
                kad_n=kad_n,
                kad_zu=kad_zu,
                geo_data=geo_data_wkt,
                geodata_center=geodata_center_wkt,
            )
            
            houses_to_create.append(house)
            
            # Вывод прогресса
            if i % 100 == 0:
                print(f"Обработано {i}/{len(filtered)} записей")

        # Массовая вставка
        if houses_to_create:
            await House.bulk_create(houses_to_create)
            print(f"УСПЕХ: Добавлено {len(houses_to_create)} домов")
        else:
            print("Все дома уже существуют в базе")

if __name__ == '__main__':
    asyncio.run(migrate_data())