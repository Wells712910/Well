import pytest
import time
from config.config import Config
from pages.login_page import LoginPage
from pages.patients_page import PatientsPage
from utils.driver_manager import DriverManager
import random


class TestAddPatient:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = DriverManager.get_driver(Config.BROWSER)
        self.driver.get(Config.BASE_URL + "/login")
        self.login_page = LoginPage(self.driver)
        self.patients_page = PatientsPage(self.driver)

        # Логинимся перед каждым тестом
        self.login_page.login(Config.EMAIL, Config.PASSWORD)
        time.sleep(2)  # Даем время для загрузки главной страницы

        yield

        # После каждого теста делаем скриншот
        test_name = self.__class__.__name__ + "_" + getattr(self, '_testMethodName', 'unknown')
        screenshot_path = f"screenshots/{test_name}_{int(time.time())}.png"
        self.driver.save_screenshot(screenshot_path)

        self.driver.quit()

    def test_add_patient_with_all_required_fields(self):
        """Тест добавления пациента с заполнением всех обязательных полей"""
        # Генерируем случайные данные
        firstname = self.patients_page.generate_random_name('male')
        surname = self.patients_page.generate_random_surname('male')
        middlename = self.patients_page.generate_random_middlename('male')
        birthday = self.patients_page.generate_random_birthday()
        phone = self.patients_page.generate_random_phone()

        print(f"Добавляем пациента: {surname} {firstname} {middlename}")
        print(f"Дата рождения: {birthday}, Телефон: {phone}")

        # Добавление пациента с ВСЕМИ обязательными полями
        self.patients_page.add_new_patient(
            firstname=firstname,
            surname=surname,
            middlename=middlename,
            birthday=birthday,
            gender="male",
            phone=phone  # Телефон теперь обязательный
        )

        # Проверка успешности сохранения
        time.sleep(2)
        is_success = self.patients_page.is_save_successful()

        assert is_success, "Пациент не был сохранен. Проверьте заполнение всех обязательных полей."

    def test_add_patient_with_all_fields_including_email(self):
        """Тест добавления пациента со всеми полями (включая email)"""
        # Генерируем случайные данные
        firstname = self.patients_page.generate_random_name('female')
        surname = self.patients_page.generate_random_surname('female')
        middlename = self.patients_page.generate_random_middlename('female')
        birthday = self.patients_page.generate_random_birthday()
        phone = self.patients_page.generate_random_phone()
        email = self.patients_page.generate_random_email()

        print(f"Добавляем пациента: {surname} {firstname} {middlename}")
        print(f"Дата рождения: {birthday}, Телефон: {phone}, Email: {email}")

        # Добавление пациента со всеми полями
        self.patients_page.add_new_patient(
            firstname=firstname,
            surname=surname,
            middlename=middlename,
            birthday=birthday,
            gender="female",
            phone=phone,
            email=email
        )

        # Проверка успешности сохранения
        time.sleep(2)
        is_success = self.patients_page.is_save_successful()

        assert is_success, "Пациент не был сохранен со всеми полями."

    def test_add_multiple_random_patients(self):
        """Тест добавления нескольких пациентов со случайными данными"""
        patients_to_add = 3
        successful_saves = 0

        for i in range(patients_to_add):
            print(f"\nДобавление пациента {i + 1}/{patients_to_add}")

            # Чередуем мужской и женский пол
            gender = 'male' if i % 2 == 0 else 'female'

            # Добавляем случайного пациента
            patient_data = self.patients_page.add_random_patient(gender)

            # Проверяем успешность
            time.sleep(1.5)
            if self.patients_page.is_save_successful():
                successful_saves += 1
                print(f"✓ Пациент {patient_data['surname']} {patient_data['firstname']} успешно добавлен")
            else:
                errors = self.patients_page.get_validation_errors()
                print(f"✗ Ошибка при добавлении пациента: {errors}")

                # Если есть ошибки, пробуем закрыть форму и начать заново
                try:
                    # Кнопка отмены или закрытия
                    cancel_button = self.driver.find_element(
                        "xpath", "//div[@role='dialog']//button[1]"
                    )
                    cancel_button.click()
                    time.sleep(0.5)
                except:
                    pass

        print(f"\nИтог: успешно добавлено {successful_saves}/{patients_to_add} пациентов")
        assert successful_saves == patients_to_add, f"Не все пациенты были добавлены. Успешно: {successful_saves}/{patients_to_add}"

    @pytest.mark.parametrize("gender", ["male", "female"])
    def test_add_patient_by_gender(self, gender):
        """Параметризованный тест добавления пациентов разного пола"""
        # Генерируем соответствующие данные
        firstname = self.patients_page.generate_random_name(gender)
        surname = self.patients_page.generate_random_surname(gender)
        middlename = self.patients_page.generate_random_middlename(gender)
        birthday = self.patients_page.generate_random_birthday()
        phone = self.patients_page.generate_random_phone()

        gender_display = "Мужской" if gender == "male" else "Женский"
        print(f"Добавляем {gender_display} пациента: {surname} {firstname}")

        self.patients_page.add_new_patient(
            firstname=firstname,
            surname=surname,
            middlename=middlename,
            birthday=birthday,
            gender=gender,
            phone=phone
        )

        time.sleep(2)
        assert self.patients_page.is_save_successful(), f"Не удалось добавить {gender_display} пациента"

    def test_add_patient_with_min_age(self):
        """Тест добавления молодого пациента (18 лет)"""
        from datetime import datetime, timedelta

        # Дата рождения ровно 18 лет назад
        today = datetime.now()
        birthday_18 = (today - timedelta(days=18 * 365)).strftime("%d.%m.%Y")

        self.patients_page.add_new_patient(
            firstname="Максим",
            surname="Молодцов",
            middlename="Александрович",
            birthday=birthday_18,
            gender="male",
            phone=self.patients_page.generate_random_phone()
        )

        time.sleep(2)
        assert self.patients_page.is_save_successful(), "Не удалось добавить молодого пациента"

    def test_add_patient_with_max_age(self):
        """Тест добавления пациента пожилого возраста (70 лет)"""
        from datetime import datetime, timedelta

        # Дата рождения 70 лет назад
        today = datetime.now()
        birthday_70 = (today - timedelta(days=70 * 365)).strftime("%d.%m.%Y")

        self.patients_page.add_new_patient(
            firstname="Василий",
            surname="Мудров",
            middlename="Петрович",
            birthday=birthday_70,
            gender="male",
            phone=self.patients_page.generate_random_phone()
        )

        time.sleep(2)
        assert self.patients_page.is_save_successful(), "Не удалось добавить пожилого пациента"

    def test_phone_number_format_validation(self):
        """Тест валидации формата номера телефона"""
        test_phones = [
            "+79991234567",  # Корректный
            "+7 (999) 123-45-67",  # Возможно, неправильный
            "89991234567",  # Без +7
            "+7999123456",  # 10 цифр вместо 11
            "+799912345678",  # 12 цифр вместо 11
        ]

        for phone in test_phones:
            print(f"Проверка номера: {phone}")

            self.patients_page.open_add_patient_form()

            # Заполняем форму
            self.patients_page.fill_patient_form(
                firstname="Тест",
                surname="Тестов",
                middlename="Тестович",
                birthday="01.01.1990",
                gender="male",
                phone=phone
            )

            self.patients_page.save_patient()
            time.sleep(1)

            errors = self.patients_page.get_validation_errors()
            if errors:
                print(f"  Ошибка: {errors}")

            # Закрываем форму для следующего теста
            try:
                cancel_button = self.driver.find_element(
                    "xpath", "//div[@role='dialog']//button[1]"
                )
                cancel_button.click()
                time.sleep(0.5)
            except:
                # Если форма закрылась сама, продолжаем
                pass


# Дополнительные утилитарные функции
def generate_test_data(count=5):
    """Генерация тестовых данных для отладки"""
    patients_page = PatientsPage(None)  # Создаем экземпляр только для генерации данных

    test_data = []
    for i in range(count):
        gender = 'male' if i % 2 == 0 else 'female'
        test_data.append({
            'firstname': patients_page.generate_random_name(gender),
            'surname': patients_page.generate_random_surname(gender),
            'middlename': patients_page.generate_random_middlename(gender),
            'birthday': patients_page.generate_random_birthday(),
            'gender': gender,
            'phone': patients_page.generate_random_phone(),
            'email': patients_page.generate_random_email()
        })

    return test_data


if __name__ == "__main__":
    # Пример генерации тестовых данных
    print("Примеры тестовых данных:")
    for i, data in enumerate(generate_test_data(3), 1):
        print(f"\nПациент {i}:")
        print(f"  ФИО: {data['surname']} {data['firstname']} {data['middlename']}")
        print(f"  Пол: {data['gender']}, Дата рождения: {data['birthday']}")
        print(f"  Телефон: {data['phone']}")
        print(f"  Email: {data['email']}")