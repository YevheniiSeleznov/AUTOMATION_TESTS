import os
from datetime import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EpamWebSite:

    def __init__(self):
        self.driver = None

    def test_title(self,driver):
        # Expected title
        expected_title = "EPAM | Software Engineering & Product Development Services"
        # Open EPAM website
        driver.get("https://www.epam.com/")
        # Get actual title
        actual_title = driver.title
        # Assert title is correct
        assert actual_title == expected_title
    def test_company_logo_navigation(self, driver):
        # Open the EPAM about page
        driver.get("https://www.epam.com/about")
        # Click on the company logo in the header
        logo_link = driver.find_element(By.XPATH, "//a[@class='header__logo']")
        logo_link.click()
        # Wait for the page to load
        driver.implicitly_wait(10)  # Adjust the wait time based on your page load time
        # Get the current URL after clicking the logo
        current_url = driver.current_url
        # Assert that the current URL is the main page URL
        assert current_url == "https://www.epam.com/", f"Expected URL: https://www.epam.com/, Actual URL: {current_url}"
        # Run the test
    test_company_logo_navigation()

    def test_epam_contact_form_validation(self, driver):
        # Open the EPAM contact page
        driver.get("https://www.epam.com/about/who-we-are/contact")
        # Locate the form elements
        name_field = driver.find_element(By.NAME, "name")
        email_field = driver.find_element(By.NAME, "email")
        message_field = driver.find_element(By.NAME, "message")
        # Submit the form without entering any data
        driver.find_element(By.XPATH, "//button[text()='Submit']").click()
        # Check for validation messages
        name_validation = name_field.find_element(By.XPATH, "../span[@class='error-message']").text
        email_validation = email_field.find_element(By.XPATH, "../span[@class='error-message']").text
        message_validation = message_field.find_element(By.XPATH, "../span[@class='error-message']").text
        # Assert that the required fields have validation messages
        assert "Required" in name_validation, f"Name field validation failed: {name_validation}"
        assert "Required" in email_validation, f"Email field validation failed: {email_validation}"
        assert "Required" in message_validation, f"Message field validation failed: {message_validation}"
    def test_download_report(self, driver):
        # Open the EPAM about page
        driver.get("https://www.epam.com/about")
        # Locate the link to download the report
        download_link = driver.find_element(By.XPATH, "//a[contains(@href,'Corporate_Overview_2023_Report')]")
        # Get the download link URL
        download_url = download_link.get_attribute("href")
        # Extract the filename from the URL
        file_name = os.path.basename(download_url)
        # Download the file
        driver.get(download_url)
        # Wait for the file to download
        time.sleep(5)
        # Check if the file exists in the Downloads directory
        downloads_directory = os.path.expanduser("~") + "/Downloads/"
        file_path = os.path.join(downloads_directory, file_name)
        # Assert that the file exists
        assert os.path.exists(file_path), f"File not found: {file_path}"
        # Assert that the file has the correct extension (adjust the expected extension)
        expected_extension = ".pdf"  # Adjust the expected extension based on the actual file type
        assert file_name.endswith(expected_extension), f"Unexpected file extension: {file_name}"
    # Run the test
    test_download_report()
    def assertEqual(self, actual_title, expected_title, param):
        pass

    def test_check_policies_list(self, driver):
        # Open EPAM.com
        driver.get("https://www.epam.com")
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the policies list to be visible
        policies_list = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".footer-policy-section"))
        )
        # Extract policy items
        policy_items = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul li")))
        # Expected policy items
        expected_policies = [
            "INVESTORS",
            "COOKIE POLICY",
            "OPEN SOURCE",
            "APPLICANT PRIVACY NOTICE",
            "PRIVACY POLICY",
            "WEB ACCESSIBILITY"
        ]
        # Check if all expected policies are present
        for expected_policy in expected_policies:
            assert any(expected_policy.lower() in policy.text.lower() for policy in policy_items), f"Expected policy '{expected_policy}' not found."
    def test_search_functionality(self,driver):
        # Open the EPAM homepage
        driver.get("https://www.epam.com/")
        # Locate the search input field
        search_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@id='headerSearch']")))
        # Type the search query "AI"
        search_input.send_keys("AI")
        # Submit the search form
        search_input.submit()
        # Wait for the search results to load (adjust the wait time based on your page load time)
        driver.implicitly_wait(10)
        # Check if the search results are displayed
        search_results = driver.find_elements(By.XPATH, "//div[@class='search-results-item']")
        assert search_results, "Search results not found for the query 'AI'"
    # Run the test
    test_search_functionality()
    def test_switch_location_list_by_region(self,driver):
        # Open EPAM.com
        global locations_list, region_name
        driver.get("https://www.epam.com")
        # Scroll to the Our Locations part
        our_locations_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Our Locations')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", our_locations_link)
        # Wait for the regions to be visible
        regions = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".location-filter a"))
        )
        # Expected regions
        expected_regions = ["AMERICAS", "EMEA", "APAC"]
        # Check that 3 regions are presented
        assert len(regions) == len(expected_regions), f"Expected {len(expected_regions)} regions, but found {len(regions)}."
        # Check that each expected region is presented
        for expected_region in expected_regions:
            assert any(expected_region in region.text for region in regions), f"Expected region '{expected_region}' not found."
        # Switch to each region and verify the locations list
        for region in regions:
            region_name = region.text.strip()
            region.click()
            locations_list = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".location-list")))

        # Check that the locations list is not empty
        assert locations_list.text.strip() != "", f"Locations list for region '{region_name}' is empty."
    # Run the test
    test_switch_location_list_by_region()
    def test_switch_theme(self,driver):
        # Open EPAM website
        driver.get("https://www.epam.com")
        # Get initial theme
        initial_theme = self.get_theme(driver)
        print(f"Initial theme: {initial_theme}")

    def test_abilitytoswitchLightDarkmode(self,driver, initial_theme=None):
        # Test name: Ability to switch Light / Dark mode
        self.driver.find_element(By.CSS_SELECTOR, ".theme-switcher-ui:nth-child(3) .switch").click()
        # Wait for theme change
        driver.implicitly_wait(5)
        # Get new theme
        new_theme = self.get_theme(driver)
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
            