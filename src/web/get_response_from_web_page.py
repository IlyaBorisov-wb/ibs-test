from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

WEB_SITE_URL = 'https://reqres.in/'
STATUS_CODE_LOCATOR = "//span[@data-key='response-code']"
RESPONSE_BODY_LOCATOR = "//pre[@data-key='output-response']"


def find_element(driver, locator):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        return element
    except:
        pass

def get_response_from_web_page(locator):


    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options)
    driver.get(WEB_SITE_URL)
    sleep(1)
    driver.find_element(By.XPATH, locator).click()
    sleep(1)
    response_code = find_element(driver, (By.XPATH, STATUS_CODE_LOCATOR))
    sleep(1)
    output_response = find_element(driver, (By.XPATH, RESPONSE_BODY_LOCATOR))
    sleep(1)
    response_code_text = response_code.text
    output_response_text = output_response.text
    driver.close()

    return response_code_text, output_response_text

