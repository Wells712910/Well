from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class VisitsPage(BasePage):
    # Локаторы меню
    VISITS_MENU = (By.XPATH, "//aside//nav[1]/div[5]")
    ADD_VISIT_BUTTON = (By.XPATH, "//button[contains(., 'Добавить визит') or contains(., 'Add visit')]")

    # Локаторы формы добавления визита
    PATIENT_DROPDOWN = (By.XPATH, "//div[contains(@class, 'dropdown') or contains(@class, 'select')][1]")
    PATIENT_OPTION = (By.ID, "dropdownItem_0")
    DATE_INPUT = (By.XPATH, "//input[@placeholder='ДД.ММ.ГГГГ']")
    DATE_PICKER_DAY = (By.XPATH, "//div[@role='dialog']//table//td[not(contains(@class, 'disabled'))]/span")
    TIME_INPUT = (By.XPATH, "//input[@placeholder='ЧЧ:ММ']")
    DOCTOR_DROPDOWN = (By.XPATH,
                       "//div[contains(text(), 'Врач') or contains(text(), 'Doctor')]/following-sibling::div//span")
    DOCTOR_OPTION = (By.XPATH, "//li[1]//span[contains(@class, 'option')]")
    PLACE_DROPDOWN = (By.XPATH, "//div[contains(text(), 'Место') or contains(text(), 'Place')]/following-sibling::div")
    PLACE_OPTION = (By.XPATH, "//li[1]//span[contains(@class, 'option')]")
    SAVE_VISIT_BUTTON = (By.XPATH, "//div[@role='dialog']//button[2]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_visits(self):
        """Переход в раздел визитов"""
        self.click(self.VISITS_MENU)
        time.sleep(0.5)  # Даем время для загрузки

    def open_add_visit_form(self):
        """Открытие формы добавления визита"""
        self.click(self.ADD_VISIT_BUTTON)

    def select_patient(self):
        """Выбор пациента из выпадающего списка"""
        self.click(self.PATIENT_DROPDOWN)
        time.sleep(0.3)
        self.click(self.PATIENT_OPTION)

    def select_date(self, date=None):
        """
        Выбор даты
        Если date не указан, выбирает первую доступную дату из календаря
        """
        date_input = self.find_element(self.DATE_INPUT)
        date_input.click()
        time.sleep(0.3)

        if date:
            # Очищаем поле и вводим дату
            date_input.send_keys(Keys.CONTROL + "a")
            date_input.send_keys(Keys.DELETE)
            date_input.send_keys(date)
        else:
            # Выбираем дату из календаря
            available_days = self.driver.find_elements(*self.DATE_PICKER_DAY)
            if available_days:
                available_days[0].click()

    def set_time(self, time_str):
        """Установка времени"""
        time_input = self.find_element(self.TIME_INPUT)
        time_input.click()
        time.sleep(0.2)
        time_input.send_keys(Keys.CONTROL + "a")
        time_input.send_keys(Keys.DELETE)
        time_input.send_keys(time_str)

    def select_doctor(self):
        """Выбор врача"""
        self.click(self.DOCTOR_DROPDOWN)
        time.sleep(0.3)
        self.click(self.DOCTOR_OPTION)

    def select_place(self):
        """Выбор места приема"""
        self.click(self.PLACE_DROPDOWN)
        time.sleep(0.3)
        self.click(self.PLACE_OPTION)

    def save_visit(self):
        """Сохранение визита"""
        self.click(self.SAVE_VISIT_BUTTON)

    def add_new_visit(self, time_str="09:00"):
        """Полный процесс добавления визита"""
        self.open_add_visit_form()
        self.select_patient()
        self.select_date()
        self.set_time(time_str)
        self.select_doctor()
        self.select_place()
        self.save_visit()