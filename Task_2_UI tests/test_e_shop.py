import pytest
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
        driver.find_element(By.ID, "FirstName").send_keys("Yevhenii")
        driver.find_element(By.ID, "LastName").send_keys("Doe")
        driver.find_element(By.ID, "Email").send_keys("Yevhenii.onSEO30@example.com")
        driver.find_element(By.ID, "Password").send_keys("Test@123")
        driver.find_element(By.ID, "ConfirmPassword").send_keys("Test@123")
        # Submit the registration form
        driver.find_element(By.CSS_SELECTOR, 'input[value="Register"]').click()
        # Wait for registration to complete
        time.sleep(3)
        # Verify that registration was successful
        success_message = driver.find_element(By.CLASS_NAME, "result").text
        assert "Your registration completed" in success_message
    def test_login_user(self, driver):
        # Navigate to the login page
        driver.get("https://demowebshop.tricentis.com/login")
        # Fill in the login form
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Email"))).send_keys("Yevhenii.onSE1O@example.com")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Password"))).send_keys("Test@123")
        # Submit the login form
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[value="Log in"]'))).click()
        # Wait for login to complete
        #time.sleep(3)
        # Verify that login was successful
        #welcome_message = WebDriverWait(driver, 10).until(
            #EC.visibility_of_element_located((By.CLASS_NAME, "topic"))).text
        #assert "Welcome, Yevhenii Doe!" in welcome_message

    def test_add_to_cart(self,driver):
        # Navigate to a product page (you can replace the URL with the desired product)
        driver.get("https://demowebshop.tricentis.com/build-your-own-expensive-computer")
        # Click the "Add to cart" button
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "topcartlink")))
        add_to_cart_button.click()
        # Wait for the success message to appear
        time.sleep(3)
        # Verify that the item is added to the cart
        cart_icon = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart-qty")))
        assert int(cart_icon.text) > 0, "Adding to cart failed"
        # Navigate to the shopping cart page
        driver.get("https://demowebshop.tricentis.com/cart")
        # Verify that the added item is in the shopping cart
        cart_items = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart .product")))
        assert len(cart_items) > 0, "Item not found in the shopping cart"
        # Close the browser
        driver.quit()

    def test_add_to_wishlist(self,driver):
        # Navigate to a product page
        driver.get("https://demowebshop.tricentis.com/build-your-own-expensive-computer")
        # Click the "Add to wishlist" button
        add_to_wishlist_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "add-to-wishlist-button-19")))
        add_to_wishlist_button.click()
        # Wait for the success message to appear
        time.sleep(3)
        # Verify that the success message is displayed
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".bar-notification.success .content"))).text
        assert "The product has been added to your wishlist" in success_message, "Adding to wishlist failed"

    def test_sort_items(self,driver):
        # Navigate to a product category
        driver.get("https://demowebshop.tricentis.com/computers")
        # Select the sorting dropdown element
        sorting_dropdown = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "products-orderby")))
        # Define the sorting option
        sorting_option = "Price: High to Low"
        # Select the sorting option from the dropdown
        sorting_dropdown.click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//option[text()='{sorting_option}']"))).click()
        # Wait for the page to load
        time.sleep(3)
        # Verify that items are sorted correctly
        sorted_items = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item .product-title")))
        item_names = [item.text for item in sorted_items]
        # Check if items are sorted in the expected order
        assert item_names == sorted(item_names), f"Items are not sorted correctly for option: {sorting_option}"
    def test_change_items_per_page(self,driver):
        # Navigate to a product category
        driver.get("https://demowebshop.tricentis.com/computers")
        # Select the items per page dropdown element
        items_per_page_dropdown = driver.find_element(By.NAME, "products-pagesize")
        # Define the options for the number of items per page
        items_per_page_options = ["3", "6", "9", "12"]
        for option in items_per_page_options:
            # Select each option from the dropdown
            items_per_page_dropdown.click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//option[text()='{option}']"))).click()
            # Wait for the page to load
            time.sleep(3)
            # Verify that the correct number of items is displayed on the page
            displayed_items = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
            assert len(displayed_items) == int(
                option), f"Number of displayed items does not match selected option: {option}"
    def test_checkout_item(self,driver):
        # Navigate to a product page
        driver.get("https://demowebshop.tricentis.com/build-your-own-expensive-computer")
        # Click the "Add to cart" button
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "add-to-cart-button-19")))
        add_to_cart_button.click()
        # Wait for the success message to appear
        time.sleep(3)
        # Click the shopping cart icon to go to the cart
        cart_icon = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart-qty")))
        cart_icon.click()
        # Click the "Go to cart" button
        go_to_cart_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart .button-1")))
        go_to_cart_button.click()
        # Click the "Checkout" button
        checkout_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "checkout")))
        checkout_button.click()
        # Wait for the checkout page to load
        time.sleep(3)
        # Verify that the checkout page is reached
        assert "checkout" in driver.current_url.lower(), "Not on the checkout page"
    def test_verify_computers_subgroups(self,driver):
        # Navigate to the Computers category
        driver.get("https://demowebshop.tricentis.com/computers")
        # Find and click on the 'Computers' category
        driver.WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Computers"))).click()
        # Wait for the page to load
        time.sleep(3)
        # Get the names of sub-groups under 'Computers'
        subgroups = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".item-box h2 a")))
        # Verify that there are 3 sub-groups with correct names
        expected_subgroup_names = ["Desktops", "Notebooks", "Accessories"]
        assert len(subgroups) == len(expected_subgroup_names), "Number of sub-groups doesn't match"
        for subgroup, expected_name in zip(subgroups, expected_subgroup_names):
            assert subgroup.text == expected_name, f"Unexpected sub-group name: {subgroup.text}"
