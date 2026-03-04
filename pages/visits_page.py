import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class VisitsPage(BasePage):
    VISITS_MENU = (By.XPATH, "//aside//nav[1]/div[5]")
    ADD_VISIT_BUTTON = (By.XPATH, "//button[contains(., 'Добавить визит') or contains(., 'Add visit')]")
    PATIENT_DROPDOWN = (By.XPATH, "//div[contains(@class,'dropdown') or contains(@class,'select')][1]")
    PATIENT_OPTION = (By.ID, "dropdownItem_0")
    DATE_INPUT = (By.XPATH, "//input[@placeholder='ДД.ММ.ГГГГ']")
    DATE_PICKER_DAY = (By.XPATH, "//div[@role='dialog']//table//td[not(contains(@class,'disabled'))]/span")
    TIME_INPUT = (By.XPATH, "//input[@placeholder='ЧЧ:ММ']")
    DOCTOR_DROPDOWN = (By.XPATH, "//div[contains(text(),'Врач') or contains(text(),'Doctor')]/following-sibling::div//span")
    DOCTOR_OPTION = (By.XPATH, "//li[1]//span[contains(@class,'option')]")
    PLACE_DROPDOWN = (By.XPATH, "//div[contains(text(),'Место') or contains(text(),'Place')]/following-sibling::div")
    PLACE_OPTION = (By.XPATH, "//li[1]//span[contains(@class,'option')]")
    SAVE_VISIT_BUTTON = (By.XPATH, "//div[@role='dialog']//button[2]")
    MODAL_DIALOG = (By.XPATH, "//div[@role='dialog']")

    def navigate_to_visits(self):
        self.click(self.VISITS_MENU)
        time.sleep(0.5)

    def open_add_visit_form(self):
        self.click(self.ADD_VISIT_BUTTON)

    def select_patient(self):
        self.click(self.PATIENT_DROPDOWN)
        time.sleep(0.3)
        self.click(self.PATIENT_OPTION)

    def select_date(self, date=None):
        date_input = self.find_element(self.DATE_INPUT)
        date_input.click()
        time.sleep(0.3)
        if date:
            date_input.send_keys(Keys.CONTROL + "a")
            date_input.send_keys(Keys.DELETE)
            date_input.send_keys(date)
        else:
            days = self.driver.find_elements(*self.DATE_PICKER_DAY)
            if days:
                days[0].click()

    def set_time(self, time_str: str):
        time_input = self.find_element(self.TIME_INPUT)
        time_input.click()
        time.sleep(0.2)
        time_input.send_keys(Keys.CONTROL + "a")
        time_input.send_keys(Keys.DELETE)
        time_input.send_keys(time_str)

    def select_doctor(self):
        self.click(self.DOCTOR_DROPDOWN)
        time.sleep(0.3)
        self.click(self.DOCTOR_OPTION)

    def select_place(self):
        self.click(self.PLACE_DROPDOWN)
        time.sleep(0.3)
        self.click(self.PLACE_OPTION)

    def save_visit(self):
        self.click(self.SAVE_VISIT_BUTTON)

    def is_save_successful(self) -> bool:
        return self.wait_for_disappear(self.MODAL_DIALOG)

    def add_new_visit(self, time_str="09:00"):
        """Полный процесс добавления визита"""
        self.open_add_visit_form()
        self.select_patient()
        self.select_date()
        self.set_time(time_str)
        self.select_doctor()
        self.select_place()
        self.save_visit()
