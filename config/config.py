from dotenv import load_dotenv
import os

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = "https://mis.qa.zabota.space"
    EMAIL = os.getenv("EMAIL", "bleyding7103@gmail.com")
    PASSWORD = os.getenv("PASSWORD", "BeuSEYUcj1Vp")
    IMPLICITLY_WAIT = 10
    PAGE_LOAD_TIMEOUT = 30
    BROWSER = os.getenv("BROWSER", "chrome")  # chrome, firefox, edge
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
        "email": "bleyding7103+test@gmail.com"
    }