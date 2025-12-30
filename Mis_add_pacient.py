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

add_pacient = ('/html/body/div/div/main/div/div/div/div[1]/div/button')

input_pacient = driver.find_element(By.XPATH,add_pacient)
input_pacient.send_keys(Keys.ENTER)

sleep(3)

client_name = ('//*[@id="firstname"]')
client_surname = ('//*[@id="surname"]')
client_patronymic = ('//*[@id="middleName"]')
client_data_birthday = ('/html/body/div[2]/div/div[2]/div/div[4]/span/input')
client_gender = ('//*[@id="gender"]')
client_gender_man = ('//*[@id="dropdownItem_0"]')
client_phone = ('//*[@id="phone"]')
client_email = ('//*[@id="email"]')
client_save_date = ('/html/body/div[2]/div/div[3]/div/button[2]')


input_client_name = driver.find_element(By.XPATH,client_name)
input_client_name.send_keys('Well')

sleep(0.5)

input_client_surname = driver.find_element(By.XPATH,client_surname)
input_client_surname.send_keys('Zell')

sleep(0.5)

input_client_patronymic = driver.find_element(By.XPATH,client_patronymic)
input_client_patronymic.send_keys('Rell')

sleep(0.5)

input_client_data_birthday = driver.find_element(By.XPATH,client_data_birthday)
input_client_data_birthday.click()

sleep(0.5)

input_client_data_birthday.click()

sleep(0.5)

input_client_data_birthday.send_keys('12.05.2003')

sleep(0.5)

input_client_gender = driver.find_element(By.XPATH,client_gender)
input_client_gender.click()

sleep(0.5)

input_client_gender_man = driver.find_element(By.XPATH,client_gender_man)
input_client_gender_man.click()

sleep(0.5)

input_client_phone = driver.find_element(By.XPATH,client_phone)
input_client_phone.send_keys('+79951564551')

sleep(0.5)

input_client_email = driver.find_element(By.XPATH,client_email)
input_client_email.send_keys('bleyding7103+test@gmail.com')

sleep(0.5)

input_save_date = driver.find_element(By.XPATH,client_save_date)
input_save_date.click()