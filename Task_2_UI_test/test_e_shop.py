import re
import time
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestEshop:
    base_url = "https://demowebshop.tricentis.com"
    def test_register_user(self,driver):
        # Navigate to the registration page
        driver.get(f"{self.base_url}/register")
        # Fill in the registration form
        random_part = ''.join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        random_email = f"{random_part}@example.com"
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "FirstName"))).send_keys("Yevhenii")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "LastName"))).send_keys("Doe")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "Email"))).send_keys(random_email)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "Password"))).send_keys("Test@123")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ConfirmPassword"))).send_keys("Test@123")
        # Submit the registration form
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[value="Register"]'))).click()
        # Verify that registration was successful
        success_message = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "result"))).text
        assert "Your registration completed" in success_message

    def test_login_user(self, driver):
        # Navigate to the login page
        driver.get(f"{self.base_url}/login")
        login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ico-login")))
        login_link.click()
        # Enter login credentials (replace with your own credentials)
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Email")))
        password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Password")))
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Log in"]')))
        email_input.send_keys("Yevhenii.onSE1O@example.com")
        password_input.send_keys("Test@123")
        login_button.click()
        # Wait for the login to complete and check if redirected to the expected page
        driver.get("https://demowebshop.tricentis.com")
        # Assert that the login was successful
        assert "Log out" in driver.page_source, "Login was not successful"

    def test_verify_computers_page(self, driver):
        # Navigate to the demo webshop site
        driver.get(self.base_url)
        # Click on the 'Computers' button in the top menu bar
        computers_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Computers")))
        computers_button.click()
        # Verify the presence of the expected categories on the 'Computers' page
        expected_categories = ["Desktops", "Notebooks", "Accessories"]
        actual_categories = driver.find_elements(By.XPATH, "//h2[@class='title']/a")
        actual_category_names = [category.text for category in actual_categories]
        assert len(actual_categories) == len(expected_categories), \
            f"Expected {len(expected_categories)} categories, but found {len(actual_categories)}"
        for expected_category in expected_categories:
            assert expected_category in actual_category_names, \
                f"Expected category '{expected_category}' not found in actual categories: {actual_category_names}"

    def test_sorting_items_byorderby(self, driver):
        driver.get(f"{self.base_url}/desktops")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-orderby"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[. = 'Name: A to Z']"))).click()
        # Wait for the page to load completely
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
        # Get all the product names
        product_names = driver.find_elements(By.CSS_SELECTOR, ".product-item .product-title")
        # Extract the first letter from each product name
        first_letters = [name.text[0] for name in product_names]
        # Check whether the first letters are sorted correctly
        assert first_letters == sorted(first_letters), "Products are not sorted correctly by the first letter of their names"
        # Click on the "Name: Z to A" option
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[. = 'Name: Z to A']"))).click()
        # Wait for the page to load completely
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
        # Get all the product names again
        product_names = driver.find_elements(By.CSS_SELECTOR, ".product-item .product-title")
        # Extract the first letter from each product name again
        first_letters = [name.text[0] for name in product_names]
        # Check whether the first letters are sorted correctly
        assert first_letters == sorted(first_letters,reverse=True), "Products are not sorted correctly by the first letter of their names in reverse order"

    def test_sorting_items_bypagesize(self, driver):
        driver.get(f"{self.base_url}/desktops")
        # Get the initial number of products displayed on the page
        initial_product_count = len(driver.find_elements(By.CSS_SELECTOR, ".product-item"))
        # Click to change the page size to 4
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-pagesize"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[. = '4']"))).click()
        expected_page_link = "https://demowebshop.tricentis.com/desktops?pagesize=4"
        actual_page_link = driver.current_url
        assert actual_page_link == expected_page_link, f"Expected page link: {expected_page_link}, but got: {actual_page_link}"
        # Get the number of products displayed on the page after changing the page size
        updated_product_count = len(driver.find_elements(By.CSS_SELECTOR, ".product-item"))
        #  Verify that the number of products after the change is not equal to the initial number of products
        assert  updated_product_count != initial_product_count, "Number of products should change after changing page size"
        # Verify that the number of products after the change is equal to the expected page size (4)
        assert updated_product_count == 4 , f"Expected 4 products per page, but got {updated_product_count}"
        # Click to change the page size to 12
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-pagesize"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[. = '12']"))).click()
        expected_page_link = "https://demowebshop.tricentis.com/desktops?pagesize=12"
        actual_page_link = driver.current_url
        assert actual_page_link == expected_page_link, f"Expected page link: {expected_page_link}, but got: {actual_page_link}"
        # Get the number of products displayed on the page after changing the page size again
        updated_product_count = len(driver.find_elements(By.CSS_SELECTOR, ".product-item"))
        # Verify that the number of products after the second change is not equal to the initial number of products
        assert updated_product_count == initial_product_count , "Number of products should change after the second page size change"
        # Verify that the number of products after the second change is equal to the expected page size (12)
        assert updated_product_count != 12, f"Expected 12 products per page, but got {updated_product_count}"

    def test_add_to_cart(self, driver):
        # Navigate to the demo webshop site
        driver.get(self.base_url)
        # Click on the 'Log in' link
        login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ico-login")))
        login_link.click()
        # Enter login credentials (replace with your own credentials)
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Email")))
        password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Password")))
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Log in"]')))
        email_input.send_keys("Yevhenii.onSE1O@example.com")
        password_input.send_keys("Test@123")
        login_button.click()
        # Navigate to the smartphone page
        driver.get(f"{self.base_url}/smartphone")
        # Click on the 'Add to Cart' button
        add_to_cart_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Add to cart"]')))
        add_to_cart_button.click()
        # Find the added item's name
        added_item_name_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.product-name')))
        added_item_name = added_item_name_element.text
        # Assert the name of the added item
        expected_item_name = "Smartphone"  # Replace with the expected name of the item
        assert added_item_name == expected_item_name, f"Expected item name: {expected_item_name}, Actual item name: {added_item_name}"
        # Navigate to the shopping cart
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cart-label'))).click()
        # Check the checkbox for the item to be removed
        remove_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "removefromcart")))
        remove_checkbox.click()
        # Click on the 'Update shopping cart' button
        update_cart_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "updatecart")))
        update_cart_button.click()
        # Wait for the cart to update
        WebDriverWait(driver, 10).until(EC.staleness_of(remove_checkbox))
        # Check if the cart is empty
        empty_cart_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.order-summary-content')))
        # Assert that the cart is empty
        assert "Your Shopping Cart is empty!" in empty_cart_message.text, "Item was not removed from the cart"

    def test_remove_item_from_cart(self, driver):
        # Navigate to the demo webshop site
        driver.get(self.base_url)
        # Click on the 'Log in' link
        login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ico-login")))
        login_link.click()
        # Enter login credentials (replace with your own credentials)
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Email")))
        password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Password")))
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Log in"]')))
        email_input.send_keys("Yevhenii.onSE1O@example.com")
        password_input.send_keys("Test@123")
        login_button.click()
        # Navigate to the smartphone page
        driver.get(f"{self.base_url}/smartphone")
        # Click on the 'Add to Cart' button
        add_to_cart_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Add to cart"]')))
        add_to_cart_button.click()
        # Wait for the cart items to be clickable
        cart_items = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cart-qty')))
        # Find all cart items
        cart_items_list = driver.find_elements(By.CSS_SELECTOR, '.cart-qty')
        # Verify the number of cart items
        assert len(cart_items_list) == 1, "Cart should contain one item after adding."
        # Navigate to the shopping cart
        driver.find_element(By.CSS_SELECTOR, '.cart-label').click()
        # Check the checkbox for the item to be removed
        remove_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "removefromcart")))
        remove_checkbox.click()
        # Click on the 'Update shopping cart' button
        update_cart_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "updatecart")))
        update_cart_button.click()
        # Wait for the cart to update
        WebDriverWait(driver, 10).until(EC.staleness_of(remove_checkbox))
        # Check if the cart is empty
        empty_cart_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.order-summary-content')))
        # Assert that the cart is empty
        assert "Your Shopping Cart is empty!" in empty_cart_message.text, "Item was not removed from the cart"

    def test_add_to_wishlist(self,driver):
        # Navigate to the login page
        driver.get(f"{self.base_url}/login")
        # Click on the 'Log in' link
        login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ico-login")))
        login_link.click()
        # Enter login credentials (replace with your own credentials)
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Email")))
        password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Password")))
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Log in"]')))
        email_input.send_keys("Yevhenii.onSE1O@example.com")
        password_input.send_keys("Test@123")
        login_button.click()
        # Navigate to the smartphone page
        driver.get(f"{self.base_url}/smartphone")
        # Click on the 'Add to Wishlist' button
        add_to_wishlist_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Add to wishlist"]')))
        add_to_wishlist_button.click()
        time.sleep(2)
        driver.get(f"{self.base_url}/wishlist")
        # Find the name of the added item
        added_item_name_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.product')))
        added_item_name = added_item_name_element.text
        # Assert the name of the added item
        expected_item_name = "Smartphone"
        assert added_item_name == expected_item_name, f"Expected item name: {expected_item_name}, Actual item name: {added_item_name}"
        # Check the checkbox for the item to be removed
        remove_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "removefromcart")))
        remove_checkbox.click()
        # Click on the 'Update shopping cart' button
        update_cart_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "updatecart")))
        update_cart_button.click()
        # Wait for the cart to update
        WebDriverWait(driver, 10).until(EC.staleness_of(remove_checkbox))
        # Check if the cart is empty
        empty_cart_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.wishlist-content')))
        # Assert that the cart is empty
        assert "The wishlist is empty!" in empty_cart_message.text, "Item was not removed from the cart"

    def test_checkout(self,driver):
        # Enter login credentials (replace with your own credentials)
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Email")))
        password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Password")))
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Log in"]')))
        email_input.send_keys("Yevhenii.onSE1O@example.com")
        password_input.send_keys("Test@123")
        login_button.click()
        # Navigate to the smartphone page
        driver.get(f"{self.base_url}/smartphone")
        # Click on the 'Add to Cart' button
        add_to_cart_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Add to cart"]')))
        add_to_cart_button.click()
        # Verify that the cart has been updated by checking for the new item
        cart_items = driver.find_elements(By.CSS_SELECTOR, '.cart-qty')
        assert len(cart_items) == 1, "Cart should contain one item after adding."
        time.sleep(2)
        # Navigate to the shopping cart
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.cart-label'))).click()
        # Check the 'Terms of Service' checkbox
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "termsofservice"))).click()
        # Click on the 'Checkout' button
        checkout_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout"))).click()
        # Click on the 'Continue' button on the address step
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".new-address-next-step-button:nth-child(1)"))).click()
        # Click on the 'Continue' button on the shipping method step
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".new-address-next-step-button:nth-child(2)"))).click()
        # Click on the 'Continue' button on the payment method step
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".shipping-method-next-step-button"))).click()
        # Click on the 'Continue' button on the payment information step
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".payment-method-next-step-button"))).click()
        # Click on the 'Continue' button on the confirm order step
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".payment-info-next-step-button"))).click()
        # Click on the 'Confirm Order' button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".confirm-order-next-step-button"))).click()
        # Verify the completion of the order process
        assert "https://demowebshop.tricentis.com/onepagecheckout" in driver.current_url
        # Check for the success message on the page
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.section.order-completed > div')))
        expected_success_message = "Your order has been successfully processed!"
        # Check for the presence of "Order number:" text
        assert expected_success_message in success_message.text, f"Expected success message not found. Actual message: {success_message.text}"
        time.sleep(2)



