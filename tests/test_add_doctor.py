from time import sleep

import pytest
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage
from pages.doctors_page import DoctorsPage
from config.config import Config


class TestAddDoctor:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = DriverManager.get_driver()
        self.driver.get(Config.BASE_URL + "/login")
        self.login_page = LoginPage(self.driver)
        self.doctors_page = DoctorsPage(self.driver)
        yield
        self.driver.quit()

    def test_add_doctor(self):
        # Логин
        self.login_page.login(Config.EMAIL, Config.PASSWORD)

        # Переход к врачам и добавление
        self.doctors_page.navigate_to_doctors()
        self.doctors_page.add_doctor(
            firstname="Anton",
            surname="Antonovsky",
            middlename="Antonovich"
        )
