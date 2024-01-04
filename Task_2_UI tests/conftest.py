import pytest
from selenium import webdriver
@pytest.fixture()
def driver_setup():
    driver = webdriver.Chrome()
    yield
    driver.close()
    driver.quit()
