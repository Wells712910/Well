from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)


driver.get('https://mis.qa.zabota.space/login')

emailxpath = ('/html/body/div/div/input[1]')
passxpath = ('/html/body/div/div/input[2]')
signinxpath = ('/html/body/div/div/button')


email = ('bleyding7103@gmail.com')
password = ('BeuSEYUcj1Vp')


input_email = driver.find_element(By.XPATH,emailxpath)
input_email.send_keys(email)

sleep(3)

input_password = driver.find_element(By.XPATH,passxpath)
input_password.send_keys(password)

sleep(3)

input_sigin = driver.find_element(By.XPATH,signinxpath)
input_sigin.send_keys(Keys.ENTER)

sleep(2)

