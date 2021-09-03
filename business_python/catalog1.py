from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os,sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from glob import glob
from random import randint

# executor_url = driver.command_executor._url
# session_id = driver.session_id

def attach_to_session(executor_url, session_id):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver



# 
def upload_each_catalog(name,category,actual_price,discounted_price,description,image_file_path):
    try:
        # //*[@id="root"]/div/div/div/div/ul/a[2]/li/div[2]/span
        # driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/button').click()
        print("clicking products")
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/ul/a[2]/li/div[2]/span').click()
        sleep(2)
        try:
            print("Clicking add new item")
            # print(driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div/div[3]/button/span[1]').get_attribute("button"))
            driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div/div[3]/button').click()
            sleep(2)
        except:
            print("skipping add new item")
        print("clicking upload image")
        #checking if upload image is clickable on which div
        # /html/body/div[7]/div[3]/div/article[2]/div[1]/div[2]/article/span/label
        # /html/body/div[7]/div[3]/div/article[2]/div[1]/div[2]/article
        # driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/article[2]/div[1]/div[2]/article/span/label').click()
        driver.find_element_by_xpath("//*[@class='tc f7 fw6 ph2 mt2 lh-title']").click()
        driver.find_element_by_xpath('//*[@id="file-upload"]')\
            .send_keys(image_file_path)
        print("clicking save button")
        # driver.find_element_by_class_name("MuiButtonBase-root MuiButton-root MuiButton-contained \
            # jss151 MuiButton-containedPrimary MuiButton-disableElevation").click()
        driver.find_element_by_xpath("//*[@class='flex justify-between w-50']/button[2]/span[1]").click()
        # /html/body/div[7]/div[3]/div/div[2]/div[2]/article[2]/button[2]/span[1]
        # MuiButtonBase-root MuiButton-root MuiButton-contained jss151 MuiButton-containedPrimary MuiButton-disableElevation
        # driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[2]/div[2]/article[2]/button[2]/span[1]').click()
    
        print("entering product name")
        # /html/body/div[7]/div[3]/div/article[2]/div[2]/div[2]
        # /html/body/div[7]/div[3]/div/article[2]/div[2]/div[2]/div[1]/div/input
        driver.find_element_by_xpath("//*[@class='MuiContainer-root MuiContainer-maxWidthSm']/div[1]/div/input").send_keys(name)
        # driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/article[2]/div[2]/div[2]/div[1]/div/input').send_keys("name")
        print("entering product actual price")
        # MuiInputBase-root MuiOutlinedInput-root MuiInputBase-fullWidth MuiInputBase-formControl
        # /html/body/div[7]/div[3]/div/article[2]/div[2]/div[2]
        driver.find_element_by_xpath("//*[@class='MuiContainer-root MuiContainer-maxWidthSm']/div[2]/div[1]/div/div/input").send_keys(actual_price)
        print("entering product discounted price")
        driver.find_element_by_xpath("//*[@class='MuiContainer-root MuiContainer-maxWidthSm']/div[2]/div[2]/div/div/input").send_keys(discounted_price)
        print("entering product category")
        driver.find_element_by_xpath("//*[@class='MuiContainer-root MuiContainer-maxWidthSm']/div[3]/div/input").send_keys(category)
        print("entering product description")
        driver.find_element_by_xpath("//*[@class='MuiContainer-root MuiContainer-maxWidthSm']/textarea").send_keys(description)
        print("saving final")
        driver.find_element_by_xpath("//*[@class='flex flex-row flex-wrap justify-between items-center pv4 h-10']/div[2]/button").click()            
    except Exception as e:
        print("ERROR!!!")
        print(str(e))
driver = None
def get_driver():
    global driver
    driver = attach_to_session('http://127.0.0.1:1103', 'd7372407c0b630f13f30af2837254081')
    driver.get('https://web.dotpe.in/login')
if __name__ == '__main__':
    category_list = {'1023_1030':'Punjabi-Patiala',\
                    '1051_1060':'Punjabi-Patiala',\
                    '1088_1090':'Salwar-Kameez',\
                    '1117_1120':'Punjabi-Patiala',\
                    '1207_1210':'Palazzo-Style',\
                    '1508_1510':'Churidar-Salwar',\
                    '1540_1550':'Boutique-Style',\
                    '1563_1570':'Embroidered',\
                    '1575_1580':'Salwar-Kameez',\
                    '1631_1640':'Gowns-Style',\
                    '1732_1740':'Churidar-Salwar',\
                    '1734_1740':'Gowns-Style',\
                    '1748_1750':'Gowns-Style',\
                    '1757_1760':'Palazzo-Style',\
                    '1893_1900':'Salwar-Kameez',\
                    '2002_2010':'Salwar-Kameez',\
                    '2087_2090':'Wedding-Wear',\
                    '2113_2120':'Salwar-Kameez',\
                    '2121_2130':'Salwar-Kameez',\
                    '2216_2220':'Palazzo-Style',\
                    '2239_2240':'Salwar-Kameez',\
                    '2462_2470':'Sharara-Style',\
                    '2468_2470':'Bollywood-Style',\
                    '2540_2550':'Wedding-Wear',\
                    '2602_2610':'Churidar-Salwar',\
                    '2646_2650':'Sharara-Style',\
                    '2847_2850':'Salwar-Kameez',\
                    '3144_3150':'Salwar-Kameez',\
                    '4249_4250':'Wedding-Wear',\
                    '880_890':'Salwar-Kameez',\
                    '997_1000':'Salwar-Kameez'}
    for folder_name in glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final","*")):
        # print("'" + folder_name.split("\\")[-1] + "':'',\\")
        for file_name in os.listdir(folder_name):
            # print(file_name + "\n")
            image_file_path = os.path.join(folder_name,file_name)
            # print(folder_name.split("\\")[-1])
            category = category_list[folder_name.split("\\")[-1]].replace("-"," ")
            # print(category)
            discounted_price = int(folder_name.split("\\")[-1].split("_")[-1])
            # print(discounted_price)
            actual_price = (discounted_price//100 + 2)*100 + randint(1,300)
            # print(actual_price)
            name = " ".join(file_name.replace("-","_").split("_")[2:]).split(".")[:1][0]
            # print(name)
            description = "Please order via dotpe and order will be recived on whatsapp"
            print(name,category,actual_price,discounted_price,description)
            get_driver()
            upload_each_catalog(name,category,actual_price,discounted_price,description,image_file_path)


