import pytest


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    yield
    driver.close()
    driver.quit()
