from selenium import webdriver
import os
driver = webdriver.Chrome(os.path.join(os.path.dirname(os.path.abspath(__file__)),"chromedriver"))

executor_url = driver.command_executor._url
session_id = driver.session_id

print(session_id)
print(executor_url)

driver.get('https://web.dotpe.in/login')