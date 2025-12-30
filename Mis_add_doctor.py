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





take_doctor = ('/html/body/div/div/aside/nav[1]/div[2]')
add_doctor = ('/html/body/div/div/main/div/div/div/div[1]/div/button/span[2]')
name_doctor = ('//*[@id="firstname"]')
surname_doctor = ('//*[@id="surname"]')
middlename_doctor = ('//*[@id="middleName"]')
save_data = ('/html/body/div[2]/div/div[3]/div/button[2]/span[2]')


input_take_doctor = driver.find_element(By.XPATH,take_doctor)
input_take_doctor.click()

sleep (0.2)

input_add_doctor = driver.find_element(By.XPATH,add_doctor)
input_add_doctor.click()

sleep(0.2)

input_name = driver.find_element(By.XPATH,name_doctor)
input_name.send_keys("Anton")

sleep(0.2)

input_surname = driver.find_element(By.XPATH,surname_doctor)
input_surname.send_keys("Antonovsky")

sleep(0.2)

input_middlename = driver.find_element(By.XPATH,middlename_doctor)
input_middlename.send_keys("Antonovich")

sleep(0.2)

input_save_data = driver.find_element(By.XPATH,save_data)
input_save_data.click()