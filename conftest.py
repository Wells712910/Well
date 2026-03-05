import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config.config import Config
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage


def pytest_configure(config):
    """Проверка env-переменных до запуска тестов"""
    Config.validate()


@pytest.fixture(scope="session")
def driver():
    """Один браузер на всю сессию."""
    _driver = DriverManager.get_driver()
    yield _driver
    _driver.quit()


@pytest.fixture(scope="session")
def logged_in_driver(driver):
    """Браузер с уже выполненным входом — логинится один раз."""
    driver.get(Config.BASE_URL + "/login")
    LoginPage(driver).login(Config.EMAIL, Config.PASSWORD)
    yield driver


@pytest.fixture(autouse=True)
def cleanup_after_test(request, driver):
    """
    После каждого теста:
    - закрывает открытые модальные окна через ESC
    - делает скриншот при падении
    """
    yield

    # Закрываем модалку если она осталась открытой
    try:
        modals = driver.find_elements(By.XPATH, "//div[@role='dialog']")
        if modals and any(m.is_displayed() for m in modals):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.5)
    except Exception:
        pass

    # Скриншот при падении
    try:
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            os.makedirs(Config.SCREENSHOTS_PATH, exist_ok=True)
            path = f"{Config.SCREENSHOTS_PATH}{request.node.name}.png"
            driver.save_screenshot(path)
            print(f"\nСкриншот сохранён: {path}")
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для доступа к результату теста в фикстурах"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)