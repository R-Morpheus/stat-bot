from dotenv import load_dotenv
import os

# Загрузка данных из файла .env
load_dotenv()

# Получение токена и других настроек из переменных окружения
TOKEN = os.getenv("TOKEN")
EXCEL_ALLOWED_USER_ID_MORPHEY = int(os.getenv("EXCEL_ALLOWED_USER_ID_MORPHEY"))
EXCEL_ALLOWED_USER_ID_CINNA = int(os.getenv("EXCEL_ALLOWED_USER_ID_CINNA"))

