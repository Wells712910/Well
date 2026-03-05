import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class VisitsPage(BasePage):
    VISITS_MENU = (By.XPATH, "//aside//nav[1]/div[5]")
    ADD_VISIT_BUTTON = (By.XPATH, "//button[contains(@class,'_add-btn_') and @aria-label='Добавить']")
    PATIENT_DROPDOWN = (By.XPATH, "//span[@data-pc-section='input' and contains(text(),'Выберите пациента')]")
    PATIENT_OPTION = (By.ID, "dropdownItem_0")
    DATE_INPUT = (By.XPATH, "//input[@aria-controls='visitAtDate_panel']")
    DATE_PICKER_DAY = (By.XPATH, "//div[@role='dialog']//table//td[not(contains(@class,'disabled'))]/span")
    TIME_INPUT = (By.XPATH, "//input[@aria-controls='visitAtTime_panel']")
    TIME_PICKER_PANEL = (By.XPATH, "//div[@data-pc-section='timepicker']")
    DOCTOR_DROPDOWN = (By.XPATH, "//span[@data-pc-section='input' and contains(text(),'Выберите врача')]")
    PLACE_DROPDOWN = (By.XPATH, "//span[@data-pc-section='input' and contains(text(),'Выберите филиал')]")
    DROPDOWN_OPTION_FIRST = (By.XPATH, "//ul[@data-pc-section='list']/li[1]")
    SAVE_VISIT_BUTTON = (By.XPATH, "//div[@role='dialog']//button[.//span[@data-pc-section='label' and text()='Сохранить']]")
    MODAL_DIALOG = (By.XPATH, "//div[@role='dialog']")
    DIALOG_MASK_READY = (By.XPATH, "//div[@data-pc-section='mask' and not(contains(@class,'overlay-enter'))]")
    # Заголовок модалки — нейтральная зона для клика, чтобы закрыть тайм-пикер
    MODAL_HEADER = (By.XPATH, "//div[@data-pc-section='header']")

    def navigate_to_visits(self):
        self._wait_for_overlay_gone()
        self.click(self.VISITS_MENU)
        time.sleep(0.5)

    def _wait_for_overlay_gone(self, timeout=8):
        """Ждём пока оверлей модалки и тайм-пикер полностью исчезнут"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//div[@data-pc-section='mask']")
                )
            )
        except Exception:
            pass

    def _wait_for_modal_animation(self, timeout=5):
        """Ждём завершения анимации открытия модалки"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.DIALOG_MASK_READY)
            )
        except Exception:
            time.sleep(1)

    def _close_time_picker(self):
        """Закрываем тайм-пикер кликом по заголовку модалки"""
        try:
            # Ждём исчезновения тайм-пикера после клика
            header = self.find_clickable_element(self.MODAL_HEADER)
            header.click()
            time.sleep(0.3)
            WebDriverWait(self.driver, 3).until(
                EC.invisibility_of_element_located(self.TIME_PICKER_PANEL)
            )
        except Exception:
            # Если не сработало — пробуем ESC
            try:
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(0.3)
            except Exception:
                pass

    def open_add_visit_form(self):
        self.click(self.ADD_VISIT_BUTTON)
        self.find_element(self.MODAL_DIALOG)
        self._wait_for_modal_animation()

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

    def set_time(self, time_str):
        time_input = self.find_element(self.TIME_INPUT)
        time_input.click()
        time.sleep(0.2)
        time_input.send_keys(Keys.CONTROL + "a")
        time_input.send_keys(Keys.DELETE)
        time_input.send_keys(time_str)
        # Закрываем тайм-пикер — иначе он перекроет следующие элементы
        self._close_time_picker()

    def select_doctor(self):
        self.click(self.DOCTOR_DROPDOWN)
        time.sleep(0.3)
        self.click(self.DROPDOWN_OPTION_FIRST)

    def select_place(self):
        self.click(self.PLACE_DROPDOWN)
        time.sleep(0.3)
        self.click(self.DROPDOWN_OPTION_FIRST)

    def save_visit(self):
        self.click(self.SAVE_VISIT_BUTTON)

    def is_save_successful(self):
        return self.wait_for_disappear(self.MODAL_DIALOG)

    def add_new_visit(self, time_str="09:00"):
        self.open_add_visit_form()
        self.select_patient()
        self.select_date()
        self.set_time(time_str)
        self.select_doctor()
        self.select_place()
        self.save_visit()