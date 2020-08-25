from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import requests
import re
import time

class Predefined():
    def __init__(self, driver):
        self.driver = driver
    def xpathvalue(self, xpath):
        element = None
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            if element is not None:
                return element
        except:
            return False
    def waitforelement(self, xpath, time):
        element = None
        try:
            wait = WebDriverWait(self.driver, timeout=time, poll_frequency=0.2, ignored_exceptions=[NoSuchElementException,
                                                                                          ElementNotVisibleException,
                                                                                          ElementNotSelectableException])
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            return False
    def doclick(self, xpath):
        element = None
        try:
            element = self.xpathvalue(xpath)
            if element != None:
                element.click()
        except:
            return False
    def Enter(self, xpath):
        element = None
        try:
            element = self.xpathvalue(xpath)
            if element != None:
                element.send_keys(Keys.ENTER)
        except:
            return False
    def typeinput(self, input, xpath):
        element = None
        try:
            element = self.xpathvalue(xpath)
            if element != None:
                element.send_keys(input)
        except:
            return False
    def recaptcha2(self, api):
        txt = self.driver.find_element(By.XPATH, '//div[@class="g-recaptcha"]').get_attribute('data-sitekey')
        curr_url = self.driver.current_url
        if txt == None:
            element = self.driver.find_element(By.XPATH, '(//iframe[contains(@src,"recaptcha")])[1]').get_attribute(
                "outerHTML")
            element = element.decode('utf-8')
            regex = "(?<=k\=).+?(?=\&)"
            txt = re.search(regex, element)
            txt = txt.group()
        url = 'https://2captcha.com/in.php'
        response = requests.get(url, params={'key': api, 'method': 'userrecaptcha', 'googlekey': txt, 'pageurl': curr_url})
        txt = response.content
        txt = txt.decode('utf-8')
        if str('OK') in txt:
            regex = "(?<=\|).+?(?=$)"
            ID = re.search(regex, txt)
            ID = ID.group()
            time.sleep(15)
            url = 'https://2captcha.com/res.php'
            response = requests.get(url, params={'key': api, 'action': 'get', 'id': ID, 'json': 0})
            txt = response.content
            txt = txt.decode('utf-8')
            while txt == 'CAPCHA_NOT_READY':
                try:
                    time.sleep(5)
                    url = 'https://2captcha.com/res.php'
                    response = requests.get(url, params={'key': api, 'action': 'get', 'id': ID, 'json': 0})
                    txt = response.content
                    txt = txt.decode('utf-8')
                except:
                    txt = response.content
                    txt = txt.decode('utf-8')
                if txt == 'ERROR_CAPTCHA_UNSOLVABLE':
                    break
        if str('OK') in txt:
            element = self.driver.find_element(By.XPATH, '//*[@name="g-recaptcha-response"]')
            regex = "(?<=\|).+?(?=$)"
            ID = re.search(regex, txt)
            ID = ID.group()
            self.driver.execute_script(f"arguments[0].innerHTML = '{ID}'", element);
