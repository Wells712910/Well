from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import string


class PatientsPage(BasePage):
    # Локаторы
    ADD_PATIENT_BUTTON = (By.XPATH, "//button[contains(., 'Добавить') or contains(., 'Add')]")
    FIRSTNAME_INPUT = (By.ID, "firstname")
    SURNAME_INPUT = (By.ID, "surname")
    MIDDLENAME_INPUT = (By.ID, "middleName")
    BIRTHDAY_CLICK = (By.ID, "birthday")
    BIRTHDAY_INPUT = (By.XPATH, "//input[@aria-controls='birthday_panel']")
    GENDER_DROPDOWN = (By.ID, "gender")
    GENDER_MAN_OPTION = (By.ID, "dropdownItem_0")
    GENDER_WOMAN_OPTION = (By.ID, "dropdownItem_1")
    PHONE_INPUT = (By.ID, "phone")
    EMAIL_INPUT = (By.ID, "email")
    SAVE_BUTTON = (By.XPATH, "//div[@role='dialog']//button[2]")

    # Локаторы для проверок
    ERROR_MESSAGE = (By.XPATH,
                     "//div[contains(@class, 'error') or contains(@class, 'validation') or contains(@class, 'invalid')]")
    REQUIRED_FIELD_ERROR = (By.XPATH, "//div[contains(text(), 'обязательно') or contains(text(), 'required')]")
    SUCCESS_MESSAGE = (By.XPATH,
                       "//div[contains(@class, 'success') or contains(@class, 'alert-success') or contains(text(), 'успешно')]")
    PATIENT_IN_LIST = (By.XPATH, "//div[contains(@class, 'patient-item') or contains(@class, 'patient-row')]")
    MODAL_DIALOG = (By.XPATH, "//div[@role='dialog' and contains(@class, 'modal')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # --- Генераторы случайных данных ---

    @staticmethod
    def generate_random_name(gender='male'):
        """Генерация случайного имени"""
        male_names = [
            'Александр', 'Дмитрий', 'Михаил', 'Андрей', 'Сергей', 'Владимир',
            'Алексей', 'Иван', 'Евгений', 'Николай', 'Роман', 'Павел', 'Константин'
        ]
        female_names = [
            'Анна', 'Елена', 'Ольга', 'Мария', 'Наталья', 'Ирина', 'Светлана',
            'Татьяна', 'Екатерина', 'Юлия', 'Анастасия', 'Виктория', 'Дарья'
        ]

        if gender == 'male':
            return random.choice(male_names)
        else:
            return random.choice(female_names)

    @staticmethod
    def generate_random_surname(gender='male'):
        """Генерация случайной фамилии"""
        male_surnames = [
            'Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов', 'Попов',
            'Васильев', 'Павлов', 'Семенов', 'Голубев', 'Виноградов', 'Богданов'
        ]
        female_surnames = [
            'Иванова', 'Петрова', 'Сидорова', 'Смирнова', 'Кузнецова', 'Попова',
            'Васильева', 'Павлова', 'Семенова', 'Голубева', 'Виноградова', 'Богданова'
        ]

        if gender == 'male':
            return random.choice(male_surnames)
        else:
            return random.choice(female_surnames)

    @staticmethod
    def generate_random_middlename(gender='male'):
        """Генерация случайного отчества"""
        male_middlenames = [
            'Александрович', 'Дмитриевич', 'Михайлович', 'Андреевич', 'Сергеевич',
            'Владимирович', 'Алексеевич', 'Иванович', 'Евгеньевич', 'Николаевич'
        ]
        female_middlenames = [
            'Александровна', 'Дмитриевна', 'Михайловна', 'Андреевна', 'Сергеевна',
            'Владимировна', 'Алексеевна', 'Ивановна', 'Евгеньевна', 'Николаевна'
        ]

        if gender == 'male':
            return random.choice(male_middlenames)
        else:
            return random.choice(female_middlenames)

    @staticmethod
    def generate_random_phone():
        """Генерация случайного номера телефона по маске +79991234567"""
        # Первые 4 цифры после +7999
        prefix = "+7999"
        # Оставшиеся 7 цифр
        suffix = ''.join(random.choices('0123456789', k=7))
        return f"{prefix}{suffix}"

    @staticmethod
    def generate_random_email(firstname=None, surname=None):
        """Генерация случайного email с возможностью использовать имя и фамилию"""
        domains = ['gmail.com', 'yandex.ru', 'mail.ru', 'outlook.com', 'rambler.ru']
        domain = random.choice(domains)

        if firstname and surname:
            # Создаем email на основе имени и фамилии
            firstname_latin = PatientsPage._cyrillic_to_latin(firstname.lower())
            surname_latin = PatientsPage._cyrillic_to_latin(surname.lower())
            username = f"{firstname_latin}.{surname_latin}"
        else:
            # Случайный username
            username = ''.join(random.choices(string.ascii_lowercase, k=8))

        # Добавляем случайные цифры для уникальности
        numbers = ''.join(random.choices('0123456789', k=3))
        return f"{username}{numbers}@{domain}"

    @staticmethod
    def _cyrillic_to_latin(text):
        """Простая транслитерация кириллицы в латиницу"""
        translit_dict = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
            'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
            'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
            'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
            'э': 'e', 'ю': 'yu', 'я': 'ya'
        }

        result = []
        for char in text:
            if char in translit_dict:
                result.append(translit_dict[char])
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def generate_random_birthday(min_age=18, max_age=70):
        """Генерация случайной даты рождения"""
        from datetime import datetime, timedelta

        # Текущая дата
        now = datetime.now()

        # Минимальный возраст (самый молодой)
        max_birth_date = now - timedelta(days=min_age * 365)
        # Максимальный возраст (самый старый)
        min_birth_date = now - timedelta(days=max_age * 365)

        # Случайная дата между ними
        random_days = random.randint(0, (max_birth_date - min_birth_date).days)
        birth_date = min_birth_date + timedelta(days=random_days)

        return birth_date.strftime("%d.%m.%Y")

    @staticmethod
    def generate_unique_email():
        """Генерация уникального email с timestamp"""
        import time
        domains = ['gmail.com', 'yandex.ru', 'mail.ru']
        username = f"patient{int(time.time())}"
        domain = random.choice(domains)
        return f"{username}@{domain}"

    def open_add_patient_form(self):
        """Открытие формы добавления пациента"""
        try:
            self.click(self.ADD_PATIENT_BUTTON)
            time.sleep(1)  # Даем время для открытия модального окна
            # Ждем появления формы
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.FIRSTNAME_INPUT)
            )
            return True
        except Exception as e:
            print(f"Ошибка при открытии формы: {e}")
            return False

    def fill_patient_form(self, firstname, surname, middlename, birthday, gender='male',
                          phone=None, email=None):
        """
        Заполнение формы пациента ВСЕМИ обязательными полями

        Args:
            firstname: Имя
            surname: Фамилия
            middlename: Отчество
            birthday: Дата рождения в формате ДД.ММ.ГГГГ
            gender: Пол ('male' или 'female')
            phone: Телефон (если None, будет сгенерирован)
            email: Email (если None, будет сгенерирован)
        """
        # Заполняем обязательные поля
        print(f"Заполняем форму: {surname} {firstname} {middlename}")

        self.send_keys(self.FIRSTNAME_INPUT, firstname)
        self.send_keys(self.SURNAME_INPUT, surname)
        self.send_keys(self.MIDDLENAME_INPUT, middlename)

        # Заполнение даты рождения
        self._fill_birthday(birthday)

        # Выбор пола
        self._select_gender(gender)

        # Заполнение телефона (обязательное поле)
        if not phone:
            phone = self.generate_random_phone()
        self.send_keys(self.PHONE_INPUT, phone)
        print(f"Телефон: {phone}")

        # Заполнение email (обязательное поле)
        if not email:
            email = self.generate_random_email(firstname, surname)
        self.send_keys(self.EMAIL_INPUT, email)
        print(f"Email: {email}")

        return phone, email

    def _fill_birthday(self, birthday):
        """Заполнение поля даты рождения"""
        try:
            # Кликаем на поле даты
            birthday_field = self.find_element(self.BIRTHDAY_CLICK)
            birthday_field.click()
            time.sleep(0.5)

            # Получаем поле ввода
            birthday_input = self.find_element(self.BIRTHDAY_INPUT)

            # Вводим дату
            birthday_input.send_keys(birthday)
            print(f"Дата рождения: {birthday}")

        except Exception as e:
            print(f"Ошибка при заполнении даты рождения: {e}")
            # Альтернативный метод - прямой ввод
            try:
                birthday_input = self.find_element(self.BIRTHDAY_INPUT)
                birthday_input.click()
                birthday_input.clear()
                birthday_input.send_keys(birthday)
            except:
                print("Не удалось заполнить дату рождения")

    def _select_gender(self, gender):
        """Выбор пола"""
        try:
            self.click(self.GENDER_DROPDOWN)
            time.sleep(0.5)

            if gender.lower() == 'male':
                self.click(self.GENDER_MAN_OPTION)
                print("Пол: мужской")
            elif gender.lower() == 'female':
                self.click(self.GENDER_WOMAN_OPTION)
                print("Пол: женский")
            else:
                raise ValueError(f"Unknown gender: {gender}")
        except Exception as e:
            print(f"Ошибка при выборе пола: {e}")

    def save_patient(self):
        """Сохранение пациента"""
        try:
            save_button = self.find_clickable_element(self.SAVE_BUTTON)
            # Проверяем, что кнопка активна
            if save_button.is_enabled():
                save_button.click()
                print("Нажата кнопка сохранения")
                time.sleep(2)  # Даем время для обработки
                return True
            else:
                print("Кнопка сохранения неактивна")
                return False
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False

    def add_new_patient(self, firstname, surname, middlename, birthday, gender='male',
                        phone=None, email=None):
        """Полный процесс добавления пациента"""
        try:
            # Открываем форму
            if not self.open_add_patient_form():
                return False, "Не удалось открыть форму"

            # Заполняем форму
            phone, email = self.fill_patient_form(
                firstname, surname, middlename, birthday, gender, phone, email
            )

            # Сохраняем
            if not self.save_patient():
                return False, "Не удалось сохранить"

            # Проверяем успешность
            is_success = self.is_save_successful()
            if is_success:
                return True, f"Пациент {surname} {firstname} успешно добавлен"
            else:
                errors = self.get_validation_errors()
                return False, f"Ошибки при сохранении: {errors}"

        except Exception as e:
            return False, f"Исключение при добавлении пациента: {e}"

    def add_random_patient(self, gender='male'):
        """Добавление пациента со случайными данными (все поля обязательные)"""
        # Генерируем случайные данные
        firstname = self.generate_random_name(gender)
        surname = self.generate_random_surname(gender)
        middlename = self.generate_random_middlename(gender)
        birthday = self.generate_random_birthday()

        # Обязательные поля
        phone = self.generate_random_phone()
        email = self.generate_random_email(firstname, surname)

        print(f"\nДобавляем случайного пациента ({gender}):")
        print(f"  ФИО: {surname} {firstname} {middlename}")
        print(f"  Дата рождения: {birthday}")
        print(f"  Телефон: {phone}")
        print(f"  Email: {email}")

        # Добавляем пациента
        success, message = self.add_new_patient(
            firstname=firstname,
            surname=surname,
            middlename=middlename,
            birthday=birthday,
            gender=gender,
            phone=phone,
            email=email
        )

        result = {
            'success': success,
            'message': message,
            'data': {
                'firstname': firstname,
                'surname': surname,
                'middlename': middlename,
                'birthday': birthday,
                'gender': gender,
                'phone': phone,
                'email': email
            }
        }

        return result

    def is_save_successful(self):
        """Проверка успешного сохранения"""
        try:
            # Ждем исчезновения модального окна
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.MODAL_DIALOG)
            )
            print("Модальное окно закрылось - сохранение успешно")
            return True
        except:
            # Проверяем наличие сообщения об ошибке
            errors = self.get_validation_errors()
            if errors:
                print(f"Обнаружены ошибки: {errors}")
                return False

            # Проверяем, может форма все еще открыта
            try:
                modal_elements = self.driver.find_elements(*self.MODAL_DIALOG)
                if modal_elements:
                    print("Модальное окно все еще открыто")
                    return False
            except:
                pass

            # Если нет модального окна и нет ошибок, считаем успешным
            print("Сохранение предположительно успешно")
            return True

    def get_validation_errors(self):
        """Получение текстов ошибок валидации"""
        errors = []
        try:
            # Ищем ошибки валидации
            error_elements = self.driver.find_elements(*self.ERROR_MESSAGE)
            for error in error_elements:
                if error.text and error.text.strip():
                    errors.append(error.text.strip())

            # Ищем сообщения об обязательных полях
            required_elements = self.driver.find_elements(*self.REQUIRED_FIELD_ERROR)
            for req in required_elements:
                if req.text and req.text.strip():
                    errors.append(req.text.strip())

            # Проверяем поля на наличие красной обводки (обычно означает ошибку)
            invalid_fields = self.driver.find_elements(
                By.XPATH, "//input[contains(@class, 'invalid') or contains(@class, 'error')]"
            )
            for field in invalid_fields:
                field_name = field.get_attribute('id') or field.get_attribute('name') or 'поле'
                errors.append(f"Ошибка в поле: {field_name}")

        except Exception as e:
            print(f"Ошибка при получении ошибок валидации: {e}")

        return list(set(errors))  # Убираем дубликаты

    def close_modal_if_open(self):
        """Закрытие модального окна если оно открыто"""
        try:
            cancel_button = self.driver.find_element(
                By.XPATH, "//div[@role='dialog']//button[1]"
            )
            cancel_button.click()
            time.sleep(0.5)
            print("Модальное окно закрыто")
            return True
        except:
            return False

    def is_modal_open(self):
        """Проверка, открыто ли модальное окно"""
        try:
            modal = self.driver.find_element(*self.MODAL_DIALOG)
            return modal.is_displayed()
        except:
            return False