import pytest
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestEshop:
    def test_register_user(self,driver):
        # Navigate to the registration page
        driver.get("https://demowebshop.tricentis.com/register")
        # Fill in the registration form
        random_part = ''.join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

        random_email = f"{random_part}@example.com"
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "FirstName"))).send_keys("Yevhenii")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "LastName"))).send_keys("Doe")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Email"))).send_keys(random_email)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Password"))).send_keys("Test@123")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "ConfirmPassword"))).send_keys("Test@123")
        # Submit the registration form
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[value="Register"]'))).click()
        # Wait for registration to complete
        time.sleep(3)
        # Verify that registration was successful
        success_message = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "result"))).text
        assert "Your registration completed" in success_message

    def test_login_user(self, driver):
        # Navigate to the login page
        driver.get("https://demowebshop.tricentis.com/login")
        random_part = ''.join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        random_email = f"{random_part}@example.com"
        # Fill in the login form
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Email"))).send_keys(random_email)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Password"))).send_keys("Test@123")
        # Submit the login form
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[value="Log in"]'))).click()

    def test_verify_computers_page(self):
        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome()
        # Navigate to the demo webshop site
        driver.get("https://demowebshop.tricentis.com")
        try:
            # Click on the 'Computers' button in the top menu bar
            computers_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Computers")))
            computers_button.click()
            # Wait for the page to load (you may want to use an explicit wait here)
            time.sleep(2)
            # Verify the presence of the expected categories on the 'Computers' page
            expected_categories = ["Desktops", "Notebooks", "Accessories"]
            actual_categories = driver.find_elements(By.XPATH, "//h2[@class='title']/a")
            actual_category_names = [category.text for category in actual_categories]
            assert actual_category_names == expected_categories, \
                f"Expected categories: {expected_categories}, Actual categories: {actual_category_names}"
            print("Test passed: Computers page has correct categories.")
        finally:
            # Close the browser window
            driver.quit()

    def test_add_to_cart_after_login(self):
        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome()

        # Navigate to the demo webshop site
        driver.get("https://demowebshop.tricentis.com")
        try:
            # Click on the 'Log in' link
            login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ico-login")))
            login_link.click()
            # Enter login credentials (replace with your own credentials)
            email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Email")))
            password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Password")))
            login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Log in"]')))
            email_input.send_keys("Yevhenii.onSE1O@example.com")
            password_input.send_keys("Test@123")
            login_button.click()
            # Wait for the login to complete (you may want to use explicit wait here)
            time.sleep(2)
            # Navigate to the smartphone page
            driver.get("https://demowebshop.tricentis.com/smartphone")
            # Click on the 'Add to Cart' button
            add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Add to cart"]')))
            add_to_cart_button.click()
            # Wait for the cart to update (you may want to use explicit wait here)
            time.sleep(2)
            # Verify that the cart has been updated by checking for the new item
            cart_items = driver.find_elements(By.CSS_SELECTOR, '.cart-qty')

            assert len(cart_items) == 1, "Cart should contain one item after adding."
            print("Test passed: Cart updated by adding a new item.")

        finally:
            # Close the browser window
            driver.quit()

    def test_remove_item_from_cart(self):
        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome()
        # Navigate to the demo webshop site
        driver.get("https://demowebshop.tricentis.com")

        try:
            # Click on the 'Log in' link
            login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ico-login")))
            login_link.click()
            # Enter login credentials (replace with your own credentials)
            email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Email")))
            password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Password")))
            login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Log in"]')))
            email_input.send_keys("Yevhenii.onSE1O@example.com")
            password_input.send_keys("Test@123")
            login_button.click()
            # Wait for the login to complete (you may want to use explicit wait here)
            time.sleep(2)
            # Navigate to the shopping cart
            driver.find_element(By.CSS_SELECTOR, '.cart-label').click()
            # Wait for the cart page to load
            time.sleep(2)
            # Check the checkbox for the item to be removed
            remove_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "removefromcart")))
            remove_checkbox.click()
            # Click on the 'Update shopping cart' button
            update_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "updatecart")))
            update_cart_button.click()
            # Wait for the cart to update (you may want to use explicit wait here)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.staleness_of(remove_checkbox))
            # Verify that an empty checkbox is present
            #empty_checkbox = driver.find_element(By.NAME, "removefromcart")
            #assert empty_checkbox.is_displayed(), "An empty checkbox should be present."
            #print("Test passed: Item removed from the cart, and an empty checkbox is present.")
        finally:
            # Close the browser window
            driver.quit()

    def test_add_to_wishlist_after_login(self,driver):
        driver = webdriver.Chrome()
        # Navigate to the login page
        driver.get("https://demowebshop.tricentis.com/login")

        try:
            # Click on the 'Log in' link
            login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ico-login")))
            login_link.click()
            # Enter login credentials (replace with your own credentials)
            email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Email")))
            password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Password")))
            login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Log in"]')))
            email_input.send_keys("Yevhenii.onSE1O@example.com")
            password_input.send_keys("Test@123")
            login_button.click()
            # Wait for the login to complete (you may want to use explicit wait here)
            time.sleep(2)
            # Navigate to the smartphone page
            driver.get("https://demowebshop.tricentis.com/smartphone")
            # Click on the 'Add to Wishlist' button
            add_to_wishlist_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[value="Add to wishlist"]')))
            add_to_wishlist_button.click()
            # Wait for the wishlist to update (you may want to use explicit wait here)
            time.sleep(2)
        finally:
            # Close the browser window
            driver.quit()


