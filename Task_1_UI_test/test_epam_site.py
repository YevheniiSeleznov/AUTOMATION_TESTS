import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_check_epam_title(setup):
    driver = setup
    expected_title = 'EPAM | Software Engineering & Product Development Services'
    actual_title = driver.title
    assert actual_title == expected_title, f"Expected title: '{expected_title}', but got '{actual_title}'"

def test_switch_theme_mode(setup):
    driver = setup

    # Wait for the toggle button to be clickable
    toggle_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.theme-switcher-ui:nth-child(3) > .theme-switcher'))
    )

    # Get the initial state of the theme
    initial_theme_state = driver.find_element(By.CSS_SELECTOR, 'html').get_attribute('data-theme')

    # Switch the theme
    toggle_button.click()

    # Wait for the theme to be applied
    WebDriverWait(driver, 10).until(
        lambda x: driver.find_element(By.CSS_SELECTOR, 'html').get_attribute('data-theme') != initial_theme_state
    )
    # Verify that the theme has changed
    new_theme_state = driver.find_element(By.CSS_SELECTOR, 'html').get_attribute('data-theme')
    assert initial_theme_state != new_theme_state, "Theme switch failed"


def test_change_language_to_ua(setup):
    driver = setup
    language_selector = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.location-selector__button .location-selector__button-white-arrow > svg')))
    language_selector.click()

    # Select Ukraine as the language
    ua_language_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.location-selector__item:nth-child(6) span')))
    ua_language_option.click()

    # Verify the language change
    current_language = language_selector.text
    assert current_language == "UA", "Language switch to UA failed"

def test_check_policies_list(setup):
    driver = setup
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    policies_list = ['INVESTORS', 'COOKIE POLICY', 'OPEN SOURCE', 'APPLICANT PRIVACY NOTICE', 'PRIVACY POLICY',
                     'WEB ACCESSIBILITY']

    for policy in policies_list:
        assert WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, policy))).is_displayed(), f"{policy} is not present in the policies list"

def test_search_function(setup):
    driver = setup

    # Open search field
    search_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-icon'))
    )
    search_icon.click()
    # Type & submit request "AI"
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.header__search-input'))
    )
    search_input.send_keys("AI")
    search_input.send_keys(Keys.RETURN)
    # Wait for search results page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.search-results'))
    )
    # Verify the site shows search results
    assert "AI" in driver.title, "Search result page not displayed"


def test_form_fields_validation(setup):
    driver = setup

    # Open the URL
    driver.get("https://www.epam.com")

    # Navigate to the contact page
    contact_url = "https://www.epam.com/about/who-we-are/contact"
    driver.get(contact_url)

    # Wait for the Submit button to be clickable
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.button-ui'))
    )

def test_logo_redirects_to_main_page(setup):
    driver = setup

    # Click on the company logo
    logo = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".desktop-logo > .header__logo-light"))
    )
    logo.click()

    # Verify the current URL
    current_url = driver.current_url
    assert current_url == "https://www.epam.com/", "Logo did not redirect to the main page"




if __name__ == "__main__":
    pytest.main()

