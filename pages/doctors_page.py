from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DoctorsPage(BasePage):
    DOCTORS_MENU = (By.XPATH, "//aside//nav[1]/div[2]")
    ADD_DOCTOR_BUTTON = (By.XPATH, "//button/span[2][contains(text(),'Добавить')]")
    FIRSTNAME_INPUT = (By.ID, "firstname")
    SURNAME_INPUT = (By.ID, "surname")
    MIDDLENAME_INPUT = (By.ID, "middleName")
    SAVE_BUTTON = (By.XPATH, "//div[3]//button[2]/span[2]")
    MODAL_DIALOG = (By.XPATH, "//div[@role='dialog']")

    def navigate_to_doctors(self):
        self.click(self.DOCTORS_MENU)

    def add_doctor(self, firstname: str, surname: str, middlename: str):
        self.click(self.ADD_DOCTOR_BUTTON)
        self.send_keys(self.FIRSTNAME_INPUT, firstname)
        self.send_keys(self.SURNAME_INPUT, surname)
        self.send_keys(self.MIDDLENAME_INPUT, middlename)
        self.click(self.SAVE_BUTTON)

    def is_save_successful(self) -> bool:
        return self.wait_for_disappear(self.MODAL_DIALOG)
