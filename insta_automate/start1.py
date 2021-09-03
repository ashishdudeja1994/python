# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.action_chains import ActionChains
# '''Firefox
# ------------'''
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from pwd import username,ins_pwd
# from get_comments import wow_string
# from time import sleep
# import os,sys
# import random
# import json

'''Chrome'''
from pwd import username,ins_pwd
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from get_comments import wow_string
from time import sleep
import os,sys,json,random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from glob import glob
from random import randint


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

class my_bot:
    def __init__(self,username,ins_pwd):
        try:
            # raise Exception
            # caps = DesiredCapabilities.FIREFOX
            # caps['marionette'] = True
            print("Retrying to attach to old sesssion")
            json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"session.json")
            # print(json_path)
            with open(json_path, 'r') as f:
                # print(f.read())
                data = json.load(f)
            # print(data['url'])
            
            print(data['url'],data['session_id'])
            self.driver = attach_to_session(data['url'],data['session_id'])
            self.driver.get("https://www.instagram.com/explore/tags/suitsalwar/")
            print("Old Chrome Session. Connection Done!!")
            
        except Exception as e:
            print("Error:" + str(e))
            print("Creating new Chrome Session")
            self.driver = webdriver.Chrome(os.path.join(os.path.dirname(os.path.abspath(__file__)),"chromedriver"))
            self.driver.get("https://instagram.com")
            url = self.driver.command_executor._url       
            session_id = self.driver.session_id 
            json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"session.json")
            with open(json_path, 'w') as f:
                json.dump({'url':url,'session_id':session_id}, f)
            print(url,session_id)
        

    def login(self):
        # self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]").click()
        # self.driver.get("https://instagram.com")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
        self.driver.find_element_by_xpath('//input[@name="username"]').click()
        # sleep(2)
        self.driver.find_element_by_xpath('//input[@name="username"]').send_keys(username)
        self.driver.find_element_by_xpath('//input[@name="password"]').click()
        # sleep(2)
        self.driver.find_element_by_xpath('//input[@name="password"]').send_keys(ins_pwd)
        self.driver.find_element_by_xpath('//input[@name="password"]').send_keys(Keys.ENTER)
    def search_goto_profile(self,insta_id):
        # self.driver.get("https://instagram.com")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]')))
        self.driver.find_element(By.XPATH, '//input[@placeholder="Search"]').send_keys(insta_id)
        for i in range(0,3):
            self.driver.find_element(By.XPATH, '//input[@placeholder="Search"]').send_keys(Keys.TAB)
            self.driver.find_element(By.XPATH, '//input[@placeholder="Search"]').send_keys(Keys.TAB)
            self.driver.find_element(By.XPATH, '//input[@placeholder="Search"]').send_keys(Keys.ENTER)
            sleep(1)
    def start_comments(self,wow_string):
        print("Starting comments")
        
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]')))
        # self.driver.find_element(By.XPATH, '//input[@placeholder="Search"]').send_keys("abcd")
        SCROLL_PAUSE_TIME = 10

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        master_url_list = []
        count = 0
        for i in range(0,200):
            try:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # print("here")
                # Wait to load page
                if i>0:
                    sleep(10)
                

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

                elems = self.driver.find_elements_by_xpath("//a[@href]")
                # print(elems)
                url_list = [elem for elem in elems if elem.get_attribute("href").find("/p/") != -1]
                final_url_list = [[x.get_attribute("href"),x] for x in url_list if x.get_attribute("href") not in master_url_list]
                # print(final_url_list)
                master_url_list.extend([x[0] for x in final_url_list])
                print(f"final_url_list:{len(final_url_list)}")
                print(f"master_url_list:{len(master_url_list)}")
                # print("here1")
                for elem in final_url_list:
                    if elem[1].get_attribute("href").find("/p/") != -1 :
                        print(elem[1].get_attribute("href"))
                        print(elem[1])
                        elem[1].send_keys(Keys.ENTER)
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Add a comment…"]')))
                        self.driver.find_element_by_xpath('//textarea[@placeholder="Add a comment…"]').click()
                        sleep(2)
                        actions = ActionChains(self.driver)
                        actions.send_keys(random.choice(wow_string))
                        actions.send_keys(Keys.ENTER)
                        actions.perform()
                        sleep(10)
                        count += 1
                print(f"Commented on {count} pics")
            except Exception as e:
                print("Error:" + str(e))
                print(f"Commented on {count} pics")
            
        # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        # element = driver.find_element_by_xpath('//input[@placeholder="Search"]')
        # self.driver.execute_script("return arguments[0].scrollIntoView(true);", element)
        
        # self.driver.find_element_by_xpath('/html/body/div[1]/section/main/header/div[2]/div/div[2]/span/span').click()
        # from selenium.webdriver.common.action_chains import ActionChains
        # # 1 comment of wow string will be applied to 4 pictures..thats why length * 4
        # # for i in range(0,4*len(wow_string)):
        # for i in range(0,1):
        #     # actions = ActionChains(self.driver)
        #     # actions.send_keys(Keys.TAB)
        #     # actions.send_keys(Keys.TAB)
        #     # actions.send_keys(Keys.TAB)
        #     # actions.send_keys(Keys.TAB)
           
        #     # actions.send_keys(Keys.TAB)
        #     # actions.send_keys(Keys.ENTER)
        #     # actions.perform()
        #     self.driver.find_element_by_xpath('/html/body/div[1]/section/main/header/div[2]/div/div[2]/span/span').send_keys(Keys.TAB)
        #     self.driver.find_element_by_xpath('/html/body/div[1]/section/main/header/div[2]/div/div[2]/span/span').send_keys(Keys.TAB)
        #     self.driver.find_element_by_xpath('/html/body/div[1]/section/main/header/div[2]/div/div[2]/span/span').send_keys(Keys.TAB)
        #     self.driver.find_element_by_xpath('/html/body/div[1]/section/main/header/div[2]/div/div[2]/span/span').send_keys(Keys.ENTER)
        #     self.driver.find_element_by_xpath('/html/body/div[1]/section/main/header/div[2]/div/div[2]/span/span').send_keys(Keys.ENTER)
        #     self.driver.find_element_by_xpath('/html/body/div[1]/section/main/header/div[2]/div/div[2]/span/span').send_keys(Keys.ENTER)
             
        # self.driver.find_element(By.XPATH, '//input[@placeholder="Search"]').send_keys(Keys.ESCAPE)
    def close_driver(self):
        self.driver.close()
        sleep(1)
        self.driver.quit()



        


my_bot_obj = my_bot(username,ins_pwd)
# sys.exit()
# my_bot_obj.login()
my_bot_obj.search_goto_profile("#suitsalwar")
sleep(10)
my_bot_obj.start_comments(wow_string)
# my_bot_obj.close_driver()
sys.exit()