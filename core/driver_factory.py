from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(browser: str):
    if browser == "chrome":
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    return webdriver.Firefox(service=Service(GeckoDriverManager().install()))