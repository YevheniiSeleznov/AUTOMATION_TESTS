from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import unittest

def test_change_language_to_ua(driver):
    # Open EPAM website
    driver.get("https://www.epam.com")

    # Click on the language selector button
    language_button = driver.find_element(By.XPATH, "//li[2]/div/div/button/span/div")
    language_button.click()

    # Click on the Ukrainian language option
    ukraine_option = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".location-selector__item:nth-child(6) span")
        )
    )
    ukraine_option.click()

    # Wait for page reload (explicit wait instead of implicit wait)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[lang='uk']"))
    )

    # Verify if at least one page element has the Ukrainian language attribute
    ukraine_elements = driver.find_elements(by=By.CSS_SELECTOR, value="[lang='uk']")
    assert len(ukraine_elements) > 0, "Page content not translated to Ukrainian!"

# Run the test
    test_change_language_to_ua()

if __name__ == "__main__":
    unittest.main()
