from selenium import webdriver
from selenium.webdriver.common.by import By


def test_switch_theme():
    # Use context manager to automatically close browser
    with webdriver.Chrome() as driver:
        # Open EPAM website
        driver.get("https://www.epam.com")

        # Get initial theme
        initial_theme = get_theme(driver)
        print(f"Initial theme: {initial_theme}")


def test_abilitytoswitchLightDarkmode(self):
    # Test name: Ability to switch Light / Dark mode
    self.driver.find_element(By.CSS_SELECTOR, ".theme-switcher-ui:nth-child(3) .switch").click()

    # Wait for theme change
    driver.implicitly_wait(5)

    # Get new theme
    new_theme = get_theme(driver)
    print(f"New theme: {new_theme}")

    # Verify theme switched
    assert new_theme != initial_theme, "Theme did not switch!"


def get_theme(driver):
    # Extract theme from body class attribute
    body_class = driver.find_element(by=By.TAG_NAME, value="body").get_attribute("class")
    theme = "Dark" if "dark-theme" in body_class else "Light"
    return theme


# Run the test
test_switch_theme()