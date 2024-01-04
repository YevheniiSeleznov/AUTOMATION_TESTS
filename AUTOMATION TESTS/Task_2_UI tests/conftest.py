from builtins import function

import pytest
from selenium import webdriver
@pytest.fixture(scope=function)
def driver_setup():
    driver = webdriver.Chrome()
    yield
    driver.close()
    driver.quit()
