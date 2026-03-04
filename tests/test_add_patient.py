import pytest
from datetime import datetime, timedelta
from config.config import Config
from pages.patients_page import PatientsPage
from utils.data_generator import DataGenerator


class TestAddPatient:
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver):
        self.driver = logged_in_driver
        self.patients_page = PatientsPage(self.driver)

    def test_add_male_patient(self):
        """Добавление пациента-мужчины"""
        data = DataGenerator.patient('male')
        success, message = self.patients_page.add_new_patient(**data)
        assert success, f"Пациент не сохранён: {message}"

    def test_add_female_patient(self):
        """Добавление пациента-женщины"""
        data = DataGenerator.patient('female')
        success, message = self.patients_page.add_new_patient(**data)
        assert success, f"Пациент не сохранён: {message}"

    @pytest.mark.parametrize("gender", ["male", "female"])
    def test_add_patient_by_gender(self, gender):
        """Параметризованный тест по полу"""
        result = self.patients_page.add_random_patient(gender)
        assert result['success'], f"Ошибка: {result['message']}"

    def test_add_patient_age_25(self):
        """Добавление пациента 25 лет"""
        birthday = (datetime.now() - timedelta(days=25 * 365)).strftime("%d.%m.%Y")
        data = DataGenerator.patient('male')
        data['birthday'] = birthday
        success, message = self.patients_page.add_new_patient(**data)
        assert success, f"Пациент 25 лет не сохранён: {message}"

    def test_add_patient_with_unique_email(self):
        """Добавление пациента с гарантированно уникальным email"""
        data = DataGenerator.patient('male')
        data['email'] = DataGenerator.unique_email()
        success, message = self.patients_page.add_new_patient(**data)
        assert success, f"Пациент с unique email не сохранён: {message}"
