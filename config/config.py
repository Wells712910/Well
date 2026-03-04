import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://mis.qa.zabota.space")
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    IMPLICITLY_WAIT = 10
    PAGE_LOAD_TIMEOUT = 30
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    SCREENSHOTS_PATH = "screenshots/"

    # Тестовые данные
    TEST_PATIENT = {
        "firstname": "Well",
        "surname": "Zell",
        "middlename": "Rell",
        "birthday": "12.05.2003",
        "gender": "male",
        "phone": "+79951564551",
        "email": "test+patient@example.com"
    }

    @classmethod
    def validate(cls):
        """Проверка обязательных переменных окружения"""
        missing = []
        if not cls.EMAIL:
            missing.append("EMAIL")
        if not cls.PASSWORD:
            missing.append("PASSWORD")
        if missing:
            raise EnvironmentError(
                f"Отсутствуют переменные окружения: {', '.join(missing)}. "
                f"Создайте файл .env на основе .env.example"
            )
