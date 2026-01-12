from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time


class PatientsPage(BasePage):
    # Локаторы
    ADD_PATIENT_BUTTON = (By.XPATH, "//button[contains(., 'Добавить') or contains(., 'Add')]")
    FIRSTNAME_INPUT = (By.ID, "firstname")
    SURNAME_INPUT = (By.ID, "surname")
    MIDDLENAME_INPUT = (By.ID, "middleName")
    BIRTHDAY_INPUT = (By.XPATH, "//input[@placeholder='ДД.ММ.ГГГГ' or contains(@class, 'date-input')]")
    GENDER_DROPDOWN = (By.ID, "gender")
    GENDER_MAN_OPTION = (By.ID, "dropdownItem_0")
    GENDER_WOMAN_OPTION = (By.ID, "dropdownItem_1")
    PHONE_INPUT = (By.ID, "phone")
    EMAIL_INPUT = (By.ID, "email")
    SAVE_BUTTON = (By.XPATH, "//div[@role='dialog']//button[2]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def open_add_patient_form(self):
        """Открытие формы добавления пациента"""
        self.click(self.ADD_PATIENT_BUTTON)

    def fill_patient_form(self, firstname, surname, middlename, birthday, gender='male',
                          phone=None, email=None):
        """
        Заполнение формы пациента

        Args:
            firstname: Имя
            surname: Фамилия
            middlename: Отчество
            birthday: Дата рождения в формате ДД.ММ.ГГГГ
            gender: Пол ('male' или 'female')
            phone: Телефон
            email: Email
        """
        self.send_keys(self.FIRSTNAME_INPUT, firstname)
        self.send_keys(self.SURNAME_INPUT, surname)
        self.send_keys(self.MIDDLENAME_INPUT, middlename)

        # Заполнение даты рождения
        self._fill_birthday(birthday)

        # Выбор пола
        self._select_gender(gender)

        # Заполнение телефона
        if phone:
            self.send_keys(self.PHONE_INPUT, phone)

        # Заполнение email
        if email:
            self.send_keys(self.EMAIL_INPUT, email)

    def _fill_birthday(self, birthday):
        """Заполнение поля даты рождения"""
        birthday_field = self.find_element(self.BIRTHDAY_INPUT)
        birthday_field.click()
        time.sleep(0.1)  # Краткая пауза для открытия календаря
        birthday_field.click()  # Клик для активации поля ввода
        birthday_field.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
        birthday_field.send_keys(Keys.DELETE)  # Удалить текст
        birthday_field.send_keys(birthday)

    def _select_gender(self, gender):
        """Выбор пола"""
        self.click(self.GENDER_DROPDOWN)

        if gender.lower() == 'male':
            self.click(self.GENDER_MAN_OPTION)
        elif gender.lower() == 'female':
            self.click(self.GENDER_WOMAN_OPTION)
        else:
            raise ValueError(f"Unknown gender: {gender}")

    def save_patient(self):
        """Сохранение пациента"""
        self.click(self.SAVE_BUTTON)

    def add_new_patient(self, firstname, surname, middlename, birthday, gender='male',
                        phone=None, email=None):
        """Полный процесс добавления пациента"""
        self.open_add_patient_form()
        self.fill_patient_form(firstname, surname, middlename, birthday, gender, phone, email)
        self.save_patient()