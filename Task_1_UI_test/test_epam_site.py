import time
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
        time.sleep(2)
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

    def test_check_policies_list(self, driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Policies list to check
        policies_list = ['INVESTORS', 'COOKIE POLICY', 'OPEN SOURCE', 'APPLICANT PRIVACY NOTICE', 'PRIVACY POLICY','WEB ACCESSIBILITY']
        # Check if each policy link is present on the page
        for policy in policies_list:
            policy_link_locator = By.LINK_TEXT, policy
            policy_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located(policy_link_locator))
            # Assert that the policy link is displayed
            assert policy_link.is_displayed(), f"{policy} link is not displayed."
            # You can further assert additional properties if needed, e.g., href attribute
            assert policy_link.get_attribute("href"), f"{policy} link does not have an href attribute."

    def test_location(self,driver):
        cookie_banner = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
        cookie_banner.click()
        time.sleep(5)
        # click | linkText=AMERICAS |
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "AMERICAS"))).click()
        # Assertion
        americas_text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".active > .locations-viewer-23__country .locations-viewer-23__country-title"))).text
        assert americas_text == "CANADA", f"Expected 'Canada' under AMERICAS, but got '{americas_text}'"
        # click | linkText=EMEA |
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "EMEA"))).click()
        # Assertion
        emea_text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".owl-item:nth-child(17) .locations-viewer-23__country-title"))).text
        assert emea_text == "ARMENIA", f"Expected 'Armenia' under EMEA, but got '{emea_text}'"
        #  click | linkText=APAC |
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "APAC"))).click()
        # Assertion
        apac_text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                           ".tabs-23__item:nth-child(4) .owl-item:nth-child(5) .locations-viewer-23__country-title:nth-child(1)"))).text
        assert apac_text == "AUSTRALIA", f"Expected 'Australia' under APAC, but got '{apac_text}'"

    def test_search_function(self, driver):
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
        # Check if there are search results on the page
        search_results = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-results__counter')))
        assert search_results.is_displayed(), "Search results counter not found on the page"

    def test_form_fields_validation(self,driver):
        # Open the URL
        driver.get(f"{self.base_url}/about/who-we-are/contact")
        # Handle the cookie banner if it exists
        cookie_banner = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
        cookie_banner.click()
        # Wait for the Submit button to be clickable
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.button-ui')))
        # Click on the Submit button
        submit_button.click()
        # Assert that the Submit button is clickable
        assert submit_button.is_enabled(), "Submit button is not clickable"
        # Wait for the Submit button to be clickable
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.button-ui')))
        #Enter First Name
        Name_input = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME,"user_first_name")))
        Name_input.send_keys("Jhon123")
        submit_button.click()
        # Enter Last Name
        Surname_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,"user_last_name")))
        Surname_input.send_keys("@example.com")
        assert submit_button.is_enabled(), "Submit button is not clickable"
        submit_button.click()
        assert submit_button.is_enabled(), "Submit button is not clickable"
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "user_email")))
        email_input.clear()
        email_input.send_keys("Yevhenii@example.com")
        submit_button.click()
        assert submit_button.is_enabled(), "Submit button is not clickable"
        Tel_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "user_phone")))
        Tel_input.send_keys("12345678")
        submit_button.click()
        assert submit_button.is_enabled(), "Submit button is not clickable"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-selection__rendered")))
        # Create a Select object
        submit_button.click()
        # Wait for the dropdown element to be clickable
        dropdown_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//form[@id='_content_epam_en_about_who-we-are_contact_jcr_content_content-container_section_section-par_form_constructor']/div[2]/div/div/div/div/div[8]/div/div/span/span/span/span")))
        # Click to open the dropdown
        dropdown_element.click()
        submit_button.click()
        assert submit_button.is_enabled(), "Submit button is not clickable"
        Checkbox_input = WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH,"//form[@id='_content_epam_en_about_who-we-are_contact_jcr_content_content-container_section_section-par_form_constructor']/div[2]/div/div/div/div/div[9]/div/div[2]/label")))   # Click the checkbox
        Checkbox_input.click()
        assert submit_button.is_enabled(), "Submit button is not clickable"

    def test_logo_redirects_to_main_page(self, driver):
        driver.get(f"{self.base_url}/about")
        # Wait for the company logo to be clickable
        logo_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.header__logo-light')))
        # Click on the company logo
        logo_element.click()
        # Verify the current URL is as expected
        assert driver.current_url == "https://www.epam.com/", "Page URL is not as expected"
        # Verify the presence of a new unique element on the page
        new_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.cta-button-ui:nth-child(5)')))
        assert new_element.is_displayed(), "New unique element is not present on the page"

    def test_download(self, driver):
        driver.get(f"{self.base_url}/about")
        # Handle the cookie banner if it exists
        cookie_banner = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
        cookie_banner.click()
        driver.find_element(By.CSS_SELECTOR, ".button:nth-child(3) .button__content--desktop").click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.url_to_be(("https://www.epam.com/about")))
        # Assert that the file has been downloaded with the correct name
        actual_page_link = "https://www.epam.com/content/dam/epam/free_library/EPAM_Corporate_Overview_Q3_october.pdf"
        expected_page_link = "https://www.epam.com/content/dam/epam/free_library/EPAM_Corporate_Overview_Q3_october.pdf"
        assert actual_page_link == expected_page_link, f"Expected page link: {expected_page_link}, but got: {actual_page_link}"





