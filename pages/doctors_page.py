from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class DoctorsPage(BasePage):
    # Локаторы
    DOCTORS_MENU = (By.XPATH, "//aside//nav[1]/div[2]")
    ADD_DOCTOR_BUTTON = (By.XPATH, "//button/span[2][contains(text(),'Добавить')]")
    FIRSTNAME_INPUT = (By.ID, "firstname")
    SURNAME_INPUT = (By.ID, "surname")
    MIDDLENAME_INPUT = (By.ID, "middleName")
    SAVE_BUTTON = (By.XPATH, "//div[3]//button[2]/span[2]")

    def navigate_to_doctors(self):
        self.click(self.DOCTORS_MENU)

    def add_doctor(self, firstname, surname, middlename):
        self.click(self.ADD_DOCTOR_BUTTON)
        self.send_keys(self.FIRSTNAME_INPUT, firstname)
        self.send_keys(self.SURNAME_INPUT, surname)
        self.send_keys(self.MIDDLENAME_INPUT, middlename)
        self.click(self.SAVE_BUTTON)