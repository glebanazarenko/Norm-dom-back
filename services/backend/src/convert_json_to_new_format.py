from pathlib import Path
import json

def convert_json_to_new_format(input_json_path, output_json_path):
    try:
        # Преобразуем пути в объекты Path
        input_path = Path(input_json_path)
        output_path = Path(output_json_path)

        # Проверяем существование входного JSON-файла
        if not input_path.exists():
            raise FileNotFoundError(f"JSON файл не найден: {input_json_path}")

        # Чтение данных из JSON-файла с поддержкой разных кодировок
        encodings_to_try = ['utf-8', 'cp1251', 'latin1']
        json_data = None

        for encoding in encodings_to_try:
            try:
                with input_path.open('r', encoding=encoding) as json_file:
                    json_data = json.load(json_file)
                print(f"Файл успешно прочитан с кодировкой {encoding}.")
                break
            except UnicodeDecodeError:
                continue

        if json_data is None:
            raise ValueError("Не удалось прочитать файл ни в одной из поддерживаемых кодировок.")

        # Преобразуем данные в новый формат
        new_data = []
        for index, item in enumerate(json_data, start=1):
            # Проверяем, является ли элемент словарём
            if not isinstance(item, dict):
                print(f"Предупреждение: Элемент {index} имеет некорректный тип ({type(item).__name__}), пропускается.")
                continue

            # Проверяем наличие и тип geodata_center
            geodata_center = item.get("geodata_center", {})
            if not isinstance(geodata_center, dict):
                print(f"Предупреждение: Пропущен элемент {index}, так как geodata_center имеет некорректный тип ({type(geodata_center).__name__}).")
                continue

            # Извлекаем координаты
            coordinates = geodata_center.get("coordinates", [None, None])
            if None in coordinates:
                print(f"Предупреждение: Пропущен элемент {index}, так как отсутствуют координаты.")
                continue

            # Меняем местами координаты (широту и долготу)
            latitude, longitude = coordinates
            fixed_coordinates = [longitude, latitude]  # Долгота первая, широта вторая

            # Создаём новую структуру
            new_item = {
                "OBJ_TYPE": item.get("OBJ_TYPE", "N/A"),
                "OnTerritoryOfMoscow": item.get("OnTerritoryOfMoscow", "N/A"),
                "ADDRESS": item.get("ADDRESS", "N/A"),
                "geodata_center": {
                    "coordinates": fixed_coordinates  # Используем исправленные координаты
                }
            }

            new_data.append(new_item)

        # Сохраняем новые данные в выходной JSON-файл
        with output_path.open('w', encoding='utf-8') as output_file:
            json.dump(new_data, output_file, ensure_ascii=False, indent=4)

        print(f"Новый JSON файл успешно создан: {output_json_path}")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {input_json_path} содержит некорректные JSON данные.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
if __name__ == "__main__":
    input_json_path = "services/backend/src/json/data-60562-2025-04-04.json"
    output_json_path = "services/frontend/public/houses.json"
    convert_json_to_new_format(input_json_path, output_json_path)