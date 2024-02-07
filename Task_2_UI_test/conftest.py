import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://demowebshop.tricentis.com/login")
    yield driver
    driver.quit()
