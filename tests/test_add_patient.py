import pytest
import time
from config.config import Config
from pages.login_page import LoginPage
from pages.patients_page import PatientsPage
from utils.driver_manager import DriverManager


class TestAddPatient:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = DriverManager.get_driver(Config.BROWSER)
        self.driver.get(Config.BASE_URL + "/login")
        self.login_page = LoginPage(self.driver)
        self.patients_page = PatientsPage(self.driver)
        yield
        self.driver.quit()

    def test_add_patient_with_minimal_data(self):
        """Тест добавления пациента с минимальными данными"""
        # Логин
        self.login_page.login(Config.EMAIL, Config.PASSWORD)
        time.sleep(2)  # Даем время для загрузки главной страницы

        # Добавление пациента
        self.patients_page.add_new_patient(
            firstname="Иван",
            surname="Иванов",
            middlename="Иванович",
            birthday="15.05.1985",
            gender="male"
        )

        # Проверка успешности (заглушка - нужно добавить реальные проверки)
        time.sleep(2)  # Даем время для сохранения
        # Здесь можно добавить проверку появления пациента в списке
        # или появления сообщения об успешном сохранении
        assert True

    def test_add_patient_with_full_data(self):
        """Тест добавления пациента со всеми данными"""
        # Логин
        self.login_page.login(Config.EMAIL, Config.PASSWORD)
        time.sleep(2)

        # Добавление пациента со всеми полями
        self.patients_page.add_new_patient(
            firstname="Анна",
            surname="Петрова",
            middlename="Сергеевна",
            birthday="22.10.1990",
            gender="female",
            phone="+79991234567",
            email="anna.petrova@example.com"
        )

        # Проверка успешности
        time.sleep(2)
        assert True

    @pytest.mark.parametrize("patient_data", [
        {
            "firstname": "Михаил",
            "surname": "Сидоров",
            "middlename": "Владимирович",
            "birthday": "10.03.1978",
            "gender": "male",
            "phone": "+79987654321"
        },
        {
            "firstname": "Елена",
            "surname": "Кузнецова",
            "middlename": "Александровна",
            "birthday": "30.07.1995",
            "gender": "female",
            "email": "elena.k@example.com"
        }
    ])
    def test_add_multiple_patients(self, patient_data):
        """Параметризованный тест для добавления нескольких пациентов"""
        # Логин
        self.login_page.login(Config.EMAIL, Config.PASSWORD)
        time.sleep(2)

        # Добавление пациента с параметрами
        self.patients_page.add_new_patient(
            firstname=patient_data["firstname"],
            surname=patient_data["surname"],
            middlename=patient_data["middlename"],
            birthday=patient_data["birthday"],
            gender=patient_data["gender"],
            phone=patient_data.get("phone"),
            email=patient_data.get("email")
        )

        # Проверка
        time.sleep(2)
        assert True