import pytest
from config.config import Config
from pages.visits_page import VisitsPage


class TestAddVisit:
    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver):
        self.driver = logged_in_driver
        self.visits_page = VisitsPage(self.driver)
        self.visits_page.navigate_to_visits()

    def test_add_visit_default_time(self):
        """Добавление визита со временем по умолчанию"""
        self.visits_page.add_new_visit(time_str="09:00")
        assert self.visits_page.is_save_successful(), "Визит не был сохранён"

    def test_add_visit_custom_time(self):
        """Добавление визита с кастомным временем"""
        self.visits_page.add_new_visit(time_str="14:30")
        assert self.visits_page.is_save_successful(), "Визит не был сохранён"

    @pytest.mark.parametrize("visit_time", ["09:00", "11:30", "15:45", "18:15"])
    def test_add_visits_different_times(self, visit_time):
        """Параметризованный тест: визиты в разное время"""
        self.visits_page.add_new_visit(time_str=visit_time)
        assert self.visits_page.is_save_successful(), \
            f"Визит на {visit_time} не был сохранён"
