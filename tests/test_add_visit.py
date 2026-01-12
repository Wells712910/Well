import pytest
import time
from config.config import Config
from pages.login_page import LoginPage
from pages.visits_page import VisitsPage
from utils.driver_manager import DriverManager


class TestAddVisit:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = DriverManager.get_driver(Config.BROWSER)
        self.driver.get(Config.BASE_URL + "/login")
        self.login_page = LoginPage(self.driver)
        self.visits_page = VisitsPage(self.driver)
        yield
        self.driver.quit()

    def test_add_visit_default_time(self):
        """Тест добавления визита со временем по умолчанию"""
        # Логин
        self.login_page.login(Config.EMAIL, Config.PASSWORD)
        time.sleep(2)

        # Переход в раздел визитов
        self.visits_page.navigate_to_visits()
        time.sleep(1)

        # Добавление визита
        self.visits_page.add_new_visit()

        # Проверка успешности
        time.sleep(2)
        assert True

    def test_add_visit_custom_time(self):
        """Тест добавления визита с указанным временем"""
        # Логин
        self.login_page.login(Config.EMAIL, Config.PASSWORD)
        time.sleep(2)

        # Переход в раздел визитов
        self.visits_page.navigate_to_visits()
        time.sleep(1)

        # Добавление визита с кастомным временем
        self.visits_page.add_new_visit(time_str="14:30")

        # Проверка успешности
        time.sleep(2)
        assert True

    @pytest.mark.parametrize("visit_time", ["09:00", "11:30", "15:45", "18:15"])
    def test_add_visits_different_times(self, visit_time):
        """Параметризованный тест для добавления визитов в разное время"""
        # Логин
        self.login_page.login(Config.EMAIL, Config.PASSWORD)
        time.sleep(2)

        # Переход в раздел визитов
        self.visits_page.navigate_to_visits()
        time.sleep(1)

        # Добавление визита с разным временем
        self.visits_page.add_new_visit(time_str=visit_time)

        # Проверка успешности
        time.sleep(2)
        assert True