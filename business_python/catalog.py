from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from time import sleep

driver = webdriver.Chrome(os.path.join(os.path.dirname(os.path.abspath(__file__)),"chromedriver"))
driver.get("https://web.dotpe.in/login")
url = driver.command_executor._url
session_id = driver.session_id
search_bar = driver.find_element_by_xpath("/html/body/div/div/div[2]/div[2]/div/div[2]/div/div/input")
search_bar.clear()
search_bar.send_keys("8447713023")
# search_bar.send_keys(Keys.RETURN)
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/button').click()
otp = int(input("enter otp:"))
otp_bar = driver.find_element_by_xpath('//*[@id="outlined-margin-normal"]')
otp_bar.clear()
otp_bar.send_keys(str(otp))
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/button').click()
print(driver.current_url)
sleep(10)
# driver.close()