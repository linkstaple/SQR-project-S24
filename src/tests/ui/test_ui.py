import pytest
from utils import WebDriver, app_urls
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By as FindBy
from selenium.common.exceptions import TimeoutException

print(app_urls.get('main'))

WAIT_TIME = 3

@pytest.fixture
def driver():
    safari_options = Options()
    return WebDriver(safari_options, WAIT_TIME)

def test_main_page_for_unauthorized_user(driver, capsys):
    driver.driver.start_client()
    driver.load_page(app_urls.get('main'))

    try:
        driver.wait.until(EC.url_contains('login'))
    except TimeoutException:
        assert False, "Expected Login page to be opened for unauthorizer user"

    try:
        assert driver.wait.until(EC.text_to_be_present_in_element((FindBy.ID, 'action-button'), "Register")), "Expected action button text to be \"Register\""
    except TimeoutException:
        assert False, f"\"#action-button\" element is not visible after {WAIT_TIME} secs"

def test_login_page_redirection(driver, capsys):
    driver.load_page(app_urls.get('login'))

    try:
        action_button = driver.wait.until(EC.element_to_be_clickable((FindBy.ID, 'action-button')))
        action_button.click()
    except TimeoutException:
        assert False, "Login page doesn't have action button"

    try:
        assert driver.wait.until(EC.url_contains('register')), "Page is not register page"
    except TimeoutException:
        assert False, "Action button didn't redirect to register page"
