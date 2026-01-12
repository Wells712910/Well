from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    # Локаторы
    EMAIL_INPUT = (By.XPATH, "//input[@placeholder='Email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Password']")
    SIGNIN_BUTTON = (By.XPATH, "//button")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def login(self, email, password):
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.SIGNIN_BUTTON)




