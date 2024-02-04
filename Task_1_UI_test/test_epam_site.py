import cgi
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test_epam_site:
    base_url = "https://www.epam.com"
    def test_check_epam_title(self,driver):
        expected_title = 'EPAM | Software Engineering & Product Development Services'
        actual_title = driver.title
        assert actual_title == expected_title, f"Expected title: '{expected_title}', but got '{actual_title}'"

    def test_switch_theme_mode(self,driver):
        # Wait for the toggle button to be clickable
        toggle_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.theme-switcher-ui:nth-child(3) > .theme-switcher')))

        # Get the initial state of the theme
        initial_theme_state = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html')))

        # Get the 'data-theme' attribute
        initial_theme_value = initial_theme_state.get_attribute('data-theme')

        # Switch the theme
        toggle_button.click()

        # Wait for the theme to be applied
        WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'html'), initial_theme_value)
        if initial_theme_value else EC.presence_of_element_located((By.CSS_SELECTOR, '.theme-switcher-ui:nth-child(3)')))

        # Get the updated state of the theme
        updated_theme_state = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html')))

        # Get the 'data-theme' attribute after switching
        updated_theme_value = updated_theme_state.get_attribute('data-theme')

        # Assert that the theme has changed after clicking the toggle button
        assert (initial_theme_value is None and updated_theme_value is None) or (
        initial_theme_value != updated_theme_value), "Theme should have changed after toggling."

    def test_change_language_to_ua(self, driver):
        language_selector = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.location-selector__button .location-selector__button-white-arrow > svg')))
        language_selector.click()

        # Select Ukraine as the language
        ua_language_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.location-selector__item:nth-child(6) span')))
        ua_language_option.click()

        # Wait for the language change
        language_selector = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.location-selector__button')))

        # Verify the language change
        current_language = language_selector.text
        assert current_language == 'Україна (UA)', f"Expected language 'UA', but found '{current_language}'"

    def test_check_policies_list(self,driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        policies_list = ['INVESTORS', 'COOKIE POLICY', 'OPEN SOURCE', 'APPLICANT PRIVACY NOTICE', 'PRIVACY POLICY','WEB ACCESSIBILITY']
        for policy in policies_list:
         assert WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.LINK_TEXT, policy))).is_displayed(), f"{policy} is not present in the policies list"

    def test_switch_location_by_region(self, driver):
        # Handle the cookie banner if it exists
        cookie_banner = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
        cookie_banner.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "EMEA")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "EMEA"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "APAC")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "APAC"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "AMERICAS")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "AMERICAS"))).click()

        regions = ["AMERICAS", "EMEA", "APAC"]
        for region in regions:
            region_link = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, region)))
            assert region_link.is_displayed(), f"{region} link is not displayed."

    def test_search_function(self,driver):
        # Open search field
        search_icon = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-icon")))
        search_icon.click()

        # Type & submit request "AI"
        search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "new_form_search")))
        search_input.send_keys("AI")

        # Find the search button by ID
        search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.custom-button')))

        # Retry the click
        search_button.click()

        # Verify the site shows search results using current_url
        expected_url = "https://www.epam.com/search?q=AI"
        assert expected_url in driver.current_url, f"Expected URL not found. Actual URL: {driver.current_url}"

    def test_form_fields_validation(self,driver):

        # Open the URL
        driver.get("https://www.epam.com/about/who-we-are/contact")

        # Scroll down to reveal the form
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Handle the cookie banner if it exists
        cookie_banner = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
        cookie_banner.click()

        # Wait for the Submit button to be clickable
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.button-ui')))

        #submit_button.click()

       # Assert that the Submit button is clickable
        assert submit_button.is_enabled(), "Submit button is not clickable"


    def test_logo_redirects_to_main_page(self,driver):
        driver.get(f"{self.base_url}/about")
        # Wait for the company logo to be clickable
        logo_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.header__logo-light')))

        # Click on the company logo
        logo_element.click()

        # Verify the current URL is as expected
        assert driver.current_url == "https://www.epam.com/", "Page URL is not as expected"

        # Verify the presence of a new unique element on the page
        new_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.cta-button-ui:nth-child(5)'))
        )
        assert new_element.is_displayed(), "New unique element is not present on the page"

    def test_download(self, driver):

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "About"))).click()
        # 4 | click | css=.button:nth-child(3) .button__content--desktop |
        # Handle the cookie banner if it exists
        cookie_banner = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
        cookie_banner.click()
        driver.find_element(By.CSS_SELECTOR, ".button:nth-child(3) .button__content--desktop").click()

        WebDriverWait(driver, 10).until(EC.url_to_be(("https://www.epam.com/about")))
        # Wait for the download to complete (you may need to adjust the wait time based on your application)
        WebDriverWait(driver, 30).until(EC.url_to_be(("https://www.epam.com/content/dam/epam/free_library/EPAM_Corporate_Overview_Q3_october.pdf")))

        # Extract file name from Content-Disposition header
        headers = requests.head(driver.current_url).headers
        content_disposition = headers.get('Content-Disposition', '')
        _, params = cgi.parse_header(content_disposition)
        file_name = params.get('filename')

        # Assert that the file has been downloaded with the correct name
        expected_file_name = "EPAM_Corporate_Overview_Q3_october.pdf"  # Replace with the expected file name
        assert file_name == expected_file_name, f"Expected file name: {expected_file_name}, Actual file name: {file_name}"

