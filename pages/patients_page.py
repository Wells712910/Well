import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.data_generator import DataGenerator


class PatientsPage(BasePage):
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
    MODAL_DIALOG = (By.XPATH, "//div[@role='dialog']")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'error') or contains(@class,'invalid')]")

    def open_add_patient_form(self) -> bool:
        try:
            self.click(self.ADD_PATIENT_BUTTON)
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.FIRSTNAME_INPUT)
            )
            return True
        except Exception as e:
            print(f"Ошибка при открытии формы: {e}")
            return False

    def fill_patient_form(self, firstname, surname, middlename, birthday,
                          gender='male', phone=None, email=None):
        self.send_keys(self.FIRSTNAME_INPUT, firstname)
        self.send_keys(self.SURNAME_INPUT, surname)
        self.send_keys(self.MIDDLENAME_INPUT, middlename)
        self._fill_birthday(birthday)
        self._select_gender(gender)
        self.send_keys(self.PHONE_INPUT, phone or DataGenerator.phone())
        self.send_keys(self.EMAIL_INPUT, email or DataGenerator.unique_email())

    def _fill_birthday(self, birthday: str):
        try:
            self.find_element(self.BIRTHDAY_CLICK).click()
            time.sleep(0.3)
            self.find_element(self.BIRTHDAY_INPUT).send_keys(birthday)
        except Exception as e:
            print(f"Ошибка при заполнении даты: {e}")

    def _select_gender(self, gender: str):
        self.click(self.GENDER_DROPDOWN)
        time.sleep(0.3)
        if gender.lower() == 'male':
            self.click(self.GENDER_MAN_OPTION)
        elif gender.lower() == 'female':
            self.click(self.GENDER_WOMAN_OPTION)
        else:
            raise ValueError(f"Неизвестный пол: {gender}")

    def save_patient(self) -> bool:
        btn = self.find_clickable_element(self.SAVE_BUTTON)
        if btn.is_enabled():
            btn.click()
            return True
        return False

    def add_new_patient(self, firstname, surname, middlename, birthday,
                        gender='male', phone=None, email=None):
        if not self.open_add_patient_form():
            return False, "Не удалось открыть форму"
        self.fill_patient_form(firstname, surname, middlename, birthday, gender, phone, email)
        if not self.save_patient():
            return False, "Кнопка сохранения неактивна"
        success = self.is_save_successful()
        if success:
            return True, f"Пациент {surname} {firstname} успешно добавлен"
        errors = self.get_validation_errors()
        return False, f"Ошибки: {errors}"

    def add_random_patient(self, gender='male') -> dict:
        data = DataGenerator.patient(gender)
        success, message = self.add_new_patient(**data)
        return {'success': success, 'message': message, 'data': data}

    def is_save_successful(self) -> bool:
        return self.wait_for_disappear(self.MODAL_DIALOG)

    def get_validation_errors(self):
        errors = []
        try:
            for el in self.driver.find_elements(*self.ERROR_MESSAGE):
                if el.text.strip():
                    errors.append(el.text.strip())
        except Exception:
            pass
        return list(set(errors))

    def is_modal_open(self) -> bool:
        return self.is_element_present(self.MODAL_DIALOG, timeout=2)

    def close_modal_if_open(self):
        try:
            btn = self.driver.find_element(By.XPATH, "//div[@role='dialog']//button[1]")
            btn.click()
            time.sleep(0.3)
        except Exception:
            pass
