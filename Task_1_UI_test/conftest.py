import pytest
from selenium import webdriver

@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.get("https://www.epam.com")
    yield driver
    driver.quit()