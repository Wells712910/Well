import pytest
from config.config import Config
from pages.doctors_page import DoctorsPage


class TestAddDoctor:
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver):
        self.driver = logged_in_driver
        self.doctors_page = DoctorsPage(self.driver)
        self.doctors_page.navigate_to_doctors()

    def test_add_doctor(self):
        """Добавление врача с корректными данными"""
        self.doctors_page.add_doctor(
            firstname="Anton",
            surname="Antonovsky",
            middlename="Antonovich"
        )
        assert self.doctors_page.is_save_successful(), "Врач не был сохранён"

    @pytest.mark.parametrize("firstname,surname,middlename", [
        ("Иван", "Иванов", "Иванович"),
        ("Мария", "Петрова", "Сергеевна"),
    ])
    def test_add_doctor_parametrized(self, firstname, surname, middlename):
        """Параметризованное добавление врачей"""
        self.doctors_page.add_doctor(firstname, surname, middlename)
        assert self.doctors_page.is_save_successful(), \
            f"Врач {surname} {firstname} не был сохранён"
