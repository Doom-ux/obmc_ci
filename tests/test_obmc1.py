import pytest
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# id = "username"
# id = "password"

@pytest.fixture()
def web_ui_link():
	return "https://127.0.0.0:2443"

@pytest.fixture()
def driver_chrome():
	options = webdriver.ChromeOptions()
	options.add_argument("-headless")
	driver = webdriver.Chrome(options=options)
	yield driver
	driver.quit()


def test_login_correct(driver_chrome, web_ui_link):
	driver_chrome.get(web_ui_link)

	driver_chrome.find_element('id', 'details-button').click()
	driver_chrome.implicitly_wait(3)
	driver_chrome.find_element('id', 'proceed-link').click()
	driver_chrome.implicitly_wait(5)

	driver_chrome.find_element('id', 'username').send_keys("root")
	driver_chrome.find_element('id', 'password').send_keys("0penBmc")
	driver_chrome.find_element('xpath', "//button[@data-test-id='login-button-submit']").click()
	driver_chrome.implicitly_wait(5)
	driver_chrome.find_element('id', 'app-header-user__BV_toggle_').click()

	try:
		logout_button = WebDriverWait(driver_chrome, 10).until(
			EC.visibility_of_element_located(('xpath', "//a[@data-test-id='appHeader-link-logout']")))

		assert logout_button.text == "Log out", "Logout button is not found."

	except TimeoutException:
		assert False, "Logout button is not exist."


def test_login_incorrect_user(driver_chrome, web_ui_link):
	driver_chrome.get(web_ui_link)

	driver_chrome.find_element('id', 'details-button').click()
	driver_chrome.implicitly_wait(3)
	driver_chrome.find_element('id', 'proceed-link').click()
	driver_chrome.implicitly_wait(5)

	driver_chrome.find_element('id', 'username').send_keys("myAdmin")
	driver_chrome.find_element('id', 'password').send_keys("0penBmc" + Keys.RETURN)
	time.sleep(5)

	try:
		login_button = WebDriverWait(driver_chrome, 10).until(
			EC.visibility_of_element_located(('xpath', "//button[@data-test-id='login-button-submit']")))

		assert login_button.text == "Log in", "Login button is not found."

	except TimeoutException:
		assert False, "Login button is not exist."


def test_account_blocking(driver_chrome, web_ui_link):

	attempts_count = 3
	driver_chrome.get(web_ui_link)

	driver_chrome.find_element('id', 'details-button').click()
	driver_chrome.implicitly_wait(3)
	driver_chrome.find_element('id', 'proceed-link').click()
	driver_chrome.implicitly_wait(5)
	
	for i in range(attempts_count):
		driver_chrome.find_element('id', 'username').send_keys("watcher")
		driver_chrome.find_element('id', 'password').send_keys("123" + Keys.RETURN)
		time.sleep(5)

	driver_chrome.find_element('id', 'username').send_keys("watcher")
	driver_chrome.find_element('id', 'password').send_keys("0penBmc1" + Keys.RETURN)
	time.sleep(5)

	try:
		login_button = WebDriverWait(driver_chrome, 10).until(
			EC.visibility_of_element_located(('xpath', "//button[@data-test-id='login-button-submit']")))

		assert login_button.text == "Log in", "Login button is not found."

	except TimeoutException:
		assert False, "Login button is not exist."


