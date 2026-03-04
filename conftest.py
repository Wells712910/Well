import os
import pytest
from config.config import Config
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage


def pytest_configure(config):
    """Проверка env-переменных до запуска тестов"""
    Config.validate()


@pytest.fixture(scope="session")
def driver():
    """
    Один браузер на всю сессию.
    Закрывается после последнего теста.
    """
    _driver = DriverManager.get_driver()
    yield _driver
    _driver.quit()


@pytest.fixture(scope="session")
def logged_in_driver(driver):
    """
    Браузер с уже выполненным входом.
    Логинится один раз на всю сессию.
    """
    driver.get(Config.BASE_URL + "/login")
    LoginPage(driver).login(Config.EMAIL, Config.PASSWORD)
    yield driver


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    """Автоматический скриншот при падении теста"""
    yield
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        os.makedirs(Config.SCREENSHOTS_PATH, exist_ok=True)
        path = f"{Config.SCREENSHOTS_PATH}{request.node.name}.png"
        driver.save_screenshot(path)
        print(f"\nСкриншот сохранён: {path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для доступа к результату теста в фикстурах"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
