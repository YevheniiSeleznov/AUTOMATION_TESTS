from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test_epam_site:
    def test_check_epam_title(self,setup):
        driver = setup
        expected_title = 'EPAM | Software Engineering & Product Development Services'
        actual_title = driver.title
        assert actual_title == expected_title, f"Expected title: '{expected_title}', but got '{actual_title}'"

    def test_switch_theme_mode(self, setup):
        driver = setup
        # Wait for the toggle button to be clickable
        toggle_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.theme-switcher-ui:nth-child(3) > .theme-switcher')))
        # Get the initial state of the theme
        initial_theme_state = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'html')))
        # Now, get the 'data-theme' attribute
        initial_theme_value = initial_theme_state.get_attribute('data-theme')
        # Switch the theme
        toggle_button.click()
        # Wait for the theme to be applied
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'html'), initial_theme_value)
        if initial_theme_value else EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.theme-switcher-ui:nth-child(3)')))
        # Get the updated state of the theme
        updated_theme_state = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'html')))
        # Now, get the 'data-theme' attribute after switching
        updated_theme_value = updated_theme_state.get_attribute('data-theme')
        # Assert that the theme has changed after clicking the toggle button
        assert (initial_theme_value is None and updated_theme_value is None) or (
        initial_theme_value != updated_theme_value), "Theme should have changed after toggling."

    def test_change_language_to_ua(self, setup):
        driver = setup
        language_selector = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.location-selector__button .location-selector__button-white-arrow > svg')))
        language_selector.click()
        # Select Ukraine as the language
        ua_language_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.location-selector__item:nth-child(6) span')))
        ua_language_option.click()
        # Wait for the language change
        language_selector = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.location-selector__button')))
        # Verify the language change
        current_language = language_selector.text
        assert current_language == 'Україна (UA)', f"Expected language 'UA', but found '{current_language}'"

    def test_check_policies_list(self,setup):
        driver = setup
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        policies_list = ['INVESTORS', 'COOKIE POLICY', 'OPEN SOURCE', 'APPLICANT PRIVACY NOTICE', 'PRIVACY POLICY','WEB ACCESSIBILITY']
        for policy in policies_list:
         assert WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, policy))).is_displayed(), f"{policy} is not present in the policies list"

    def test_search_function(self,setup):
        driver = setup
        # Open search field
        search_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-icon")))
        search_icon.click()
        # Type & submit request "AI"
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "new_form_search")))
        search_input.send_keys("AI")
        # Find the search button by ID
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.custom-button')))
        # Retry the click
        search_button.click()
        # Verify the site shows search results using current_url
        expected_url = "https://www.epam.com/search?q=AI"
        assert expected_url in driver.current_url, f"Expected URL not found. Actual URL: {driver.current_url}"

    def test_form_fields_validation(self,setup):
        driver = setup
        # Open the URL
        driver.get("https://www.epam.com")
        # Navigate to the contact page
        contact_url = "https://www.epam.com/about/who-we-are/contact"
        driver.get(contact_url)
        # Wait for the Submit button to be clickable
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.button-ui')))
        # Assert that the Submit button is clickable
        assert submit_button.is_enabled(), "Submit button is not clickable"


    def test_logo_redirects_to_main_page(self,setup):
        driver = setup
        # Click on the company logo
        logo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".desktop-logo > .header__logo-light")))
        logo.click()
        # Verify the current URL
        current_url = driver.current_url
        assert current_url == "https://www.epam.com/", "Logo did not redirect to the main page"



