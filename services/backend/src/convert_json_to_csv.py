from pathlib import Path
import csv
import json

def convert_json_to_csv(json_file_path, csv_file_path):
    try:
        # Преобразуем пути в объекты Path
        json_path = Path(json_file_path)
        csv_path = Path(csv_file_path)

        # Проверяем существование JSON-файла
        if not json_path.exists():
            raise FileNotFoundError(f"JSON файл не найден: {json_file_path}")

        # Чтение данных из JSON-файла с поддержкой разных кодировок
        encodings_to_try = ['utf-8', 'cp1251', 'latin1']
        json_data = None

        for encoding in encodings_to_try:
            try:
                with json_path.open('r', encoding=encoding) as json_file:
                    json_data = json.load(json_file)
                print(f"Файл успешно прочитан с кодировкой {encoding}.")
                break
            except UnicodeDecodeError:
                continue

        if json_data is None:
            raise ValueError("Не удалось прочитать файл ни в одной из поддерживаемых кодировок.")

        # Проверяем, существует ли директория для выходного файла
        output_dir = csv_path.parent
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)  # Создаём директорию, если её нет

        # Открытие CSV-файла для записи
        with csv_path.open(mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Latitude', 'Longitude', 'Description', 'Label', 'Placemark number']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
            
            # Запись заголовков
            writer.writeheader()
            
            # Конвертация каждого объекта из JSON
            for index, item in enumerate(json_data, start=1):
                # Проверяем наличие необходимых ключей
                if not isinstance(item, dict) or 'geodata_center' not in item:
                    print(f"Предупреждение: Пропущен элемент {index}, так как его структура некорректна.")
                    continue

                try:
                    latitude, longitude = item['geodata_center'].get('coordinates', [None, None])
                    simple_address = item.get('SIMPLE_ADDRESS', 'N/A')
                    adm_area = item.get('ADM_AREA', 'N/A')
                    district = item.get('DISTRICT', 'N/A')

                    description = f"Адрес: {simple_address}, Область: {adm_area}, Район: {district}"
                    label = simple_address

                    writer.writerow({
                        'Latitude': latitude,
                        'Longitude': longitude,
                        'Description': f'"{description}"',
                        'Label': f'"{label}"',
                        'Placemark number': index
                    })
                except Exception as e:
                    print(f"Ошибка при обработке элемента {index}: {e}")

        print(f"CSV файл успешно создан: {csv_file_path}")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {json_file_path} содержит некорректные JSON данные.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
if __name__ == "__main__":
    json_file_path = "services/backend/src/json/data-60562-2025-04-04.json"
    csv_file_path = "services/backend/csv/output.csv"
    convert_json_to_csv(json_file_path, csv_file_path)