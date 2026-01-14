import pytest
import time
from config.config import Config
from pages.login_page import LoginPage
from pages.patients_page import PatientsPage
from utils.driver_manager import DriverManager
from datetime import datetime, timedelta


class TestAddPatient:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = DriverManager.get_driver(Config.BROWSER)
        self.driver.get(Config.BASE_URL + "/login")
        self.login_page = LoginPage(self.driver)
        self.patients_page = PatientsPage(self.driver)

        # Логинимся перед каждым тестом
        self.login_page.login(Config.EMAIL, Config.PASSWORD)
        time.sleep(3)  # Даем время для загрузки главной страницы

        yield

        # После каждого теста делаем скриншот
        try:
            test_name = self.__class__.__name__ + "_" + getattr(self, '_testMethodName', 'unknown')
            screenshot_path = f"screenshots/{test_name}_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Скриншот сохранен: {screenshot_path}")
        except:
            pass

        self.driver.quit()

    def test_add_patient_with_all_mandatory_fields(self):
        """Тест добавления пациента с заполнением всех обязательных полей"""
        print("\n" + "=" * 60)
        print("Тест: Добавление пациента с ВСЕМИ обязательными полями")
        print("=" * 60)

        # Генерируем случайные данные с обязательными полями
        firstname = self.patients_page.generate_random_name('male')
        surname = self.patients_page.generate_random_surname('male')
        middlename = self.patients_page.generate_random_middlename('male')
        birthday = self.patients_page.generate_random_birthday()
        phone = self.patients_page.generate_random_phone()
        email = self.patients_page.generate_random_email(firstname, surname)

        print(f"\nТестовые данные:")
        print(f"  ФИО: {surname} {firstname} {middlename}")
        print(f"  Дата рождения: {birthday}")
        print(f"  Телефон: {phone}")
        print(f"  Email: {email}")

        # Добавление пациента с ВСЕМИ обязательными полями
        success, message = self.patients_page.add_new_patient(
            firstname=firstname,
            surname=surname,
            middlename=middlename,
            birthday=birthday,
            gender="male",
            phone=phone,
            email=email
        )

        print(f"\nРезультат: {message}")

        # Проверка успешности сохранения
        assert success, f"Пациент не был сохранен. Ошибка: {message}"

        # Дополнительная проверка
        time.sleep(1)
        is_success = self.patients_page.is_save_successful()
        assert is_success, "Проверка успешности сохранения не пройдена"

    def test_add_female_patient_with_all_fields(self):
        """Тест добавления женщины-пациента со всеми обязательными полями"""
        print("\n" + "=" * 60)
        print("Тест: Добавление женщины-пациента")
        print("=" * 60)

        # Генерируем женские данные
        firstname = self.patients_page.generate_random_name('female')
        surname = self.patients_page.generate_random_surname('female')
        middlename = self.patients_page.generate_random_middlename('female')
        birthday = self.patients_page.generate_random_birthday()
        phone = self.patients_page.generate_random_phone()
        email = self.patients_page.generate_random_email(firstname, surname)

        print(f"\nТестовые данные:")
        print(f"  ФИО: {surname} {firstname} {middlename}")
        print(f"  Дата рождения: {birthday}")
        print(f"  Телефон: {phone}")
        print(f"  Email: {email}")

        success, message = self.patients_page.add_new_patient(
            firstname=firstname,
            surname=surname,
            middlename=middlename,
            birthday=birthday,
            gender="female",
            phone=phone,
            email=email
        )

        print(f"\nРезультат: {message}")
        assert success, f"Пациент не был сохранен. Ошибка: {message}"

    def test_add_multiple_random_patients(self):
        """Тест добавления нескольких пациентов со случайными данными"""
        print("\n" + "=" * 60)
        print("Тест: Добавление нескольких пациентов")
        print("=" * 60)

        patients_to_add = 2  # Уменьшаем для стабильности
        successful_saves = 0
        failed_saves = []

        for i in range(patients_to_add):
            print(f"\n--- Пациент {i + 1}/{patients_to_add} ---")

            # Чередуем мужской и женский пол
            gender = 'male' if i % 2 == 0 else 'female'

            # Добавляем случайного пациента
            result = self.patients_page.add_random_patient(gender)

            if result['success']:
                successful_saves += 1
                print(f"✓ Успешно: {result['message']}")
            else:
                failed_saves.append(result['message'])
                print(f"✗ Ошибка: {result['message']}")

                # Закрываем форму если она осталась открытой
                if self.patients_page.is_modal_open():
                    self.patients_page.close_modal_if_open()

            # Пауза между добавлениями
            time.sleep(2)

        print(f"\n{'=' * 60}")
        print(f"Итог: успешно добавлено {successful_saves}/{patients_to_add} пациентов")
        if failed_saves:
            print(f"Ошибки: {failed_saves}")

        assert successful_saves == patients_to_add, f"Не все пациенты были добавлены. Успешно: {successful_saves}/{patients_to_add}"

    @pytest.mark.parametrize("gender", ["male", "female"])
    def test_add_patient_by_gender(self, gender):
        """Параметризованный тест добавления пациентов разного пола"""
        gender_display = "мужчина" if gender == "male" else "женщина"
        print(f"\nТест: Добавление {gender_display}-пациента")

        # Добавляем случайного пациента с указанным полом
        result = self.patients_page.add_random_patient(gender)

        assert result['success'], f"Не удалось добавить {gender_display}-пациента. Ошибка: {result['message']}"

    def test_add_patient_with_specific_age(self):
        """Тест добавления пациента конкретного возраста"""
        print("\n" + "=" * 60)
        print("Тест: Добавление пациента конкретного возраста")
        print("=" * 60)

        # Дата рождения 25 лет назад
        today = datetime.now()
        birthday_25 = (today - timedelta(days=25 * 365)).strftime("%d.%m.%Y")

        # Генерируем данные
        firstname = self.patients_page.generate_random_name('male')
        surname = self.patients_page.generate_random_surname('male')
        middlename = self.patients_page.generate_random_middlename('male')
        phone = self.patients_page.generate_random_phone()
        email = self.patients_page.generate_random_email(firstname, surname)

        print(f"\nТестовые данные (25 лет):")
        print(f"  ФИО: {surname} {firstname} {middlename}")
        print(f"  Дата рождения: {birthday_25}")
        print(f"  Телефон: {phone}")
        print(f"  Email: {email}")

        success, message = self.patients_page.add_new_patient(
            firstname=firstname,
            surname=surname,
            middlename=middlename,
            birthday=birthday_25,
            gender="male",
            phone=phone,
            email=email
        )

        assert success, f"Не удалось добавить пациента 25 лет. Ошибка: {message}"

    def test_add_patient_with_unique_email(self):
        """Тест добавления пациента с уникальным email"""
        print("\n" + "=" * 60)
        print("Тест: Добавление пациента с уникальным email")
        print("=" * 60)

        # Генерируем данные
        firstname = "Уникальный"
        surname = "Тестов"
        middlename = "Пользователь"
        birthday = "15.05.1990"

        # Уникальный email с timestamp
        unique_email = f"unique.patient{int(time.time())}@test.com"
        phone = self.patients_page.generate_random_phone()

        print(f"\nТестовые данные:")
        print(f"  ФИО: {surname} {firstname} {middlename}")
        print(f"  Дата рождения: {birthday}")
        print(f"  Телефон: {phone}")
        print(f"  Email: {unique_email}")

        success, message = self.patients_page.add_new_patient(
            firstname=firstname,
            surname=surname,
            middlename=middlename,
            birthday=birthday,
            gender="male",
            phone=phone,
            email=unique_email
        )

        assert success, f"Не удалось добавить пациента с уникальным email. Ошибка: {message}"



# Утилита для демонстрации генерации данных
def demonstrate_data_generation():
    """Демонстрация генерации тестовых данных"""
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ГЕНЕРАЦИИ ТЕСТОВЫХ ДАННЫХ")
    print("=" * 60)

    # Создаем экземпляр только для генерации данных
    patients_page = PatientsPage(None)

    print("\n1. Мужские пациенты:")
    for i in range(3):
        firstname = patients_page.generate_random_name('male')
        surname = patients_page.generate_random_surname('male')
        middlename = patients_page.generate_random_middlename('male')
        email = patients_page.generate_random_email(firstname, surname)
        print(f"  {surname} {firstname} {middlename} - {email}")

    print("\n2. Женские пациенты:")
    for i in range(3):
        firstname = patients_page.generate_random_name('female')
        surname = patients_page.generate_random_surname('female')
        middlename = patients_page.generate_random_middlename('female')
        email = patients_page.generate_random_email(firstname, surname)
        print(f"  {surname} {firstname} {middlename} - {email}")

    print("\n3. Телефоны:")
    for i in range(5):
        print(f"  {patients_page.generate_random_phone()}")

    print("\n4. Даты рождения:")
    for i in range(3):
        print(f"  {patients_page.generate_random_birthday()}")


if __name__ == "__main__":
    # Запуск демонстрации
    demonstrate_data_generation()