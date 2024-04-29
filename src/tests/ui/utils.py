from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By as FindBy

APP_ORIGIN_URL = 'http://127.0.0.1:8000'

app_urls = {
    'main': APP_ORIGIN_URL + '/',
    'login': APP_ORIGIN_URL + '/login',
    'register': APP_ORIGIN_URL + '/register',
    'profile': APP_ORIGIN_URL + '/profile',
}

class WebDriver:
    driver: webdriver.Safari

    def __init__(self, browser_options: Options, wait_time):
        self.driver = webdriver.Safari(options=browser_options)
        self.driver.set_window_size(1200, 800)
        self.wait = WebDriverWait(self.driver, wait_time)

    def find_element_by_id(self, id: str):
        return self.driver.find_element(FindBy.ID, id)
    
    def find_element_by_tag(self, tag_name: str):
        return self.driver.find_element(FindBy.TAG_NAME, tag_name)
    
    def load_page(self, url: str):
        self.driver.get(url)

    def wait_for(self, secs: float):
        return WebDriverWait(self.driver, secs)
