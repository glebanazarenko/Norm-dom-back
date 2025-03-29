import os
import time
import zipfile
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from src.main import logger

# Путь для загрузки файлов
download_dir = os.path.abspath("services/backend/src/json")

def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Без графического интерфейса
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    
    # Создаем уникальную временную директорию для --user-data-dir
    temp_user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_user_data_dir}")
    
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver, temp_user_data_dir
    except Exception as e:
        logger.error(f"Ошибка при инициализации WebDriver: {e}")
        raise

def download_json(driver, version):
    url = f"https://data.mos.ru/opendata/7705031674-adresniy-reestr-zdaniy-i-soorujeniy-v-gorode-moskve?pageSize=10&pageIndex=0&version=3&release={version}"
    driver.get(url)
    
    try:
        export_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Экспорт')]"))
        )
        export_button.click()
        
        json_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'JSON')]]"))
        )
        json_button.click()
        
        start_time = time.time()
        while time.time() - start_time < 60:
            for file in os.listdir(download_dir):
                if file.endswith(".zip"):
                    logger.info(f"Файл {file} успешно скачан.")
                    return os.path.join(download_dir, file)
            time.sleep(2)
        
        logger.info("Файл не скачался за 60 секунд, пробуем другую версию.")
        return None
    except Exception as e:
        logger.error(f"Ошибка при скачивании: {e}")
        return None

def extract_zip(file_path):
    if file_path and os.path.exists(file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(download_dir)
        os.remove(file_path)
        logger.info(f"Файл {file_path} успешно распакован и удален.")
    else:
        logger.warning("Файл не найден для распаковки.")

def main():
    driver, temp_user_data_dir = setup_driver()
    version = 1345
    
    try:
        while version >= 1300:
            zip_file = download_json(driver, version)
            if zip_file:
                extract_zip(zip_file)
                break  # Успешная загрузка, выходим из цикла
            version -= 1  # Переход к предыдущей версии
    finally:
        # Закрываем драйвер
        driver.quit()
        
        # Удаляем временную директорию
        if os.path.exists(temp_user_data_dir):
            shutil.rmtree(temp_user_data_dir)
            logger.info(f"Временная директория {temp_user_data_dir} успешно удалена.")

if __name__ == "__main__":
    main()