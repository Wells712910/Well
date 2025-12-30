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



take_visit = ('/html/body/div/div/aside/nav[1]/div[5]/span')
add_visit = ('/html/body/div/div/main/div/div/div/div[1]/div/button')

input_take_visit = driver.find_element(By.XPATH,take_visit)
input_take_visit.click()

sleep(0.2)

input_add_visit = driver.find_element(By.XPATH,add_visit)
input_add_visit.click()

choose_pacientv = ('/html/body/div[2]/div/div[2]/div/div[1]/div/div[3]')
pacient = ('//*[@id="dropdownItem_0"]')
add_day = ('/html/body/div[2]/div/div[2]/div/div[2]/span/input')
take_day = ('/html/body/div[2]/div/div[2]/div/div[2]/span/div/div/div/div[2]/table/tbody/tr[3]/td[4]/span')
add_time = ('/html/body/div[2]/div/div[2]/div/div[3]/span/input')
add_doctor = ('/html/body/div[2]/div/div[2]/div/div[4]/div/span')
take_doctor = ('/html/body/div[2]/div/div[2]/div/div[4]/div/div[4]/div[2]/ul/li[1]/span')
place_clinic = ('/html/body/div[2]/div/div[2]/div/div[5]/div/div[3]')
take_place = ('/html/body/div[2]/div/div[2]/div/div[5]/div/div[4]/div[2]/ul/li/span')
save_info = ('/html/body/div[2]/div/div[3]/div/button[2]')
miss_click = ('/html/body/div[2]/div/div[2]/div/div[2]/label')

input_choose_pacient = driver.find_element(By.XPATH,choose_pacientv)
input_choose_pacient.click()

sleep(0.2)

input_pacient = driver.find_element(By.XPATH,pacient)
input_pacient.click()

sleep(0.2)

input_add_day = driver.find_element(By.XPATH,add_day)
input_add_day.click()

sleep(0.2)

input_take_day = driver.find_element(By.XPATH,take_day)
input_take_day.click()

sleep(0.2)

input_add_time = driver.find_element(By.XPATH,add_time)
input_add_time.click()
sleep(0.2)
input_add_time.send_keys('09:05')

input_miss_click = driver.find_element(By.XPATH,miss_click)
input_miss_click.click()

sleep(0.2)

input_add_doctor = driver.find_element(By.XPATH,add_doctor)
input_add_doctor.click()

sleep(0.2)

input_take_doctor = driver.find_element(By.XPATH,take_doctor)
input_take_doctor.click()

sleep(0.2)

input_place_clinic = driver.find_element(By.XPATH,place_clinic)
input_place_clinic.click()

sleep(0.2)

input_take_place = driver.find_element(By.XPATH,take_place)
input_take_place.click()

sleep(0.2)

input_save_info = driver.find_element(By.XPATH,save_info)
input_save_info.click()