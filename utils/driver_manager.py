from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from config.config import Config


class DriverManager:
    @staticmethod
    def get_driver(browser=None):
        """
        Получение драйвера для указанного браузера.
        Если browser не указан — берёт из Config.
        """
        browser = (browser or Config.BROWSER).lower()

        if browser == "chrome":
            return DriverManager._get_chrome_driver()
        elif browser == "firefox":
            return DriverManager._get_firefox_driver()
        elif browser == "edge":
            return DriverManager._get_edge_driver()
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser}. Допустимые: chrome, firefox, edge")

    @staticmethod
    def _get_chrome_driver():
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        })

        if Config.HEADLESS:
            options.add_argument("--headless=new")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.implicitly_wait(Config.IMPLICITLY_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        return driver

    @staticmethod
    def _get_firefox_driver():
        options = FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        driver.maximize_window()
        driver.implicitly_wait(Config.IMPLICITLY_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        return driver

    @staticmethod
    def _get_edge_driver():
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        if Config.HEADLESS:
            options.add_argument("--headless=new")

        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
        driver.implicitly_wait(Config.IMPLICITLY_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        return driver
