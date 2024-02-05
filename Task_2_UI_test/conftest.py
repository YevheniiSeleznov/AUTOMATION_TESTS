import pytest
from selenium import webdriver

@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.get("https://demowebshop.tricentis.com/login")
    yield driver
    driver.close()
    driver.quit()

