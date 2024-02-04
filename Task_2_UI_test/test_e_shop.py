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

        # Wait for registration to complete
        time.sleep(3)

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
        assert actual_category_names == expected_categories, \
        f"Expected categories: {expected_categories}, Actual categories: {actual_category_names}"

    def test_sorting_tems(self,driver):
        # 1 | open | /desktops |
        driver.get(f"{self.base_url}/desktops")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-orderby"))).click()
        # 2 | select | id=products-orderby | label=Name: A to Z
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-orderby")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[. = 'Name: A to Z']"))).click()
        expected_page_link = "https://demowebshop.tricentis.com/desktops?orderby=5"
        actual_page_link = driver.current_url
        assert actual_page_link == expected_page_link, f"Expected page link: {expected_page_link}, but got: {actual_page_link}"
        # 3 | click | id=products-orderby |
        dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-orderby")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[. = 'Name: Z to A']"))).click()
        expected_page_link = "https://demowebshop.tricentis.com/desktops?orderby=6"
        actual_page_link = driver.current_url
        assert actual_page_link == expected_page_link, f"Expected page link: {expected_page_link}, but got: {actual_page_link}"
        # 4 | click | id=products-pagesize |
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-pagesize"))).click()
        # 5 | select | id=products-pagesize | label=4
        dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-pagesize")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[. = '4']"))).click()
        expected_page_link = "https://demowebshop.tricentis.com/desktops?orderby=6&pagesize=4"
        actual_page_link = driver.current_url
        assert actual_page_link == expected_page_link, f"Expected page link: {expected_page_link}, but got: {actual_page_link}"
        # 6 | click | id=products-pagesize |
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-pagesize"))).click()
        # 7 | select | id=products-pagesize | label=12
        dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-pagesize")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[. = '12']"))).click()
        expected_page_link = "https://demowebshop.tricentis.com/desktops?orderby=6&pagesize=12"
        actual_page_link = driver.current_url
        assert actual_page_link == expected_page_link, f"Expected page link: {expected_page_link}, but got: {actual_page_link}"

    def test_page_view(self, driver):
        # 1 | open | /desktops |
        driver.get(f"{self.base_url}/desktops?orderby=6&pagesize=4")
        # 2 | click | id=products-viewmode |
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-viewmode"))).click()
        # 3 | select | id=products-viewmode | label=List
        dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-viewmode")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[. = 'List']"))).click()
        expected_page_link = "https://demowebshop.tricentis.com/desktops?orderby=6&pagesize=4&viewmode=list"
        actual_page_link = driver.current_url
        assert actual_page_link == expected_page_link, f"Expected page link: {expected_page_link}, but got: {actual_page_link}"
        # 4 | click | id=products-viewmode |
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-viewmode"))).click()
        # 5 | select | id=products-viewmode | label=Grid
        dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "products-viewmode")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[. = 'Grid']"))).click()
        expected_page_link = "https://demowebshop.tricentis.com/desktops?orderby=6&pagesize=4&viewmode=grid"
        actual_page_link = driver.current_url
        assert actual_page_link == expected_page_link, f"Expected page link: {expected_page_link}, but got: {actual_page_link}"


    def test_add_to_cart_after_login(self, driver):
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
        driver.get("https://demowebshop.tricentis.com/smartphone")

        # Click on the 'Add to Cart' button
        add_to_cart_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Add to cart"]')))
        add_to_cart_button.click()

        # Verify that the cart has been updated by checking for the new item
        cart_items = driver.find_elements(By.CSS_SELECTOR, '.cart-qty')
        assert len(cart_items) == 1, "Cart should contain one item after adding."

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

    def test_add_to_wishlist_after_login(self,driver):
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
        driver.get("https://demowebshop.tricentis.com/smartphone")

        # Click on the 'Add to Wishlist' button
        add_to_wishlist_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[value="Add to wishlist"]')))
        add_to_wishlist_button.click()

        # Verify that the cart has been updated by checking for the new item
        wishlist_items = driver.find_elements(By.CSS_SELECTOR, '.wishlist-qty')
        assert len(wishlist_items) == 1, "Wishlist should contain one item after adding."
        print("Test passed: Wishlist updated by adding a new item.")

    def test_complete_checkout_process(self,driver):
        # Navigate to the demo webshop site
        driver.get(self.base_url)

        # Click on the 'Log in' link
        login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ico-login")))
        login_link.click()

        # Enter login credentials (replace with your own credentials)
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Email")))
        password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Password")))
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Log in"]')))
        email_input.send_keys("Yevhenii.onSE1O@example.com")
        password_input.send_keys("Test@123")
        login_button.click()

        # Navigate to the smartphone page
        driver.get("https://demowebshop.tricentis.com/smartphone")

        # Click on the 'Add to Cart' button
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Add to cart"]')))
        add_to_cart_button.click()

        # Verify that the cart has been updated by checking for the new item
        cart_items = driver.find_elements(By.CSS_SELECTOR, '.cart-qty')
        assert len(cart_items) == 1, "Cart should contain one item after adding."

        # Navigate to the shopping cart
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.cart-label'))).click()

        # Check the 'Terms of Service' checkbox
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "termsofservice"))).click()
        time.sleep(2)

        # Click on the 'Checkout' button
        checkout_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout"))).click()
        # Wait for the checkout page to load

        # Click on the 'Continue' button on the address step
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".new-address-next-step-button:nth-child(1)")))


        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".new-address-next-step-button:nth-child(1)"))).click()

        # Click on the 'Continue' button on the shipping method step
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".new-address-next-step-button:nth-child(2)")))

        #driver.execute_script("arguments[0].scrollIntoView();", element)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".new-address-next-step-button:nth-child(2)"))).click()

        # Click on the 'Continue' button on the payment method step
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".shipping-method-next-step-button")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".shipping-method-next-step-button"))).click()

        # Click on the 'Continue' button on the payment information step
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".payment-method-next-step-button")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".payment-method-next-step-button"))).click()

        # Click on the 'Continue' button on the confirm order step
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".payment-info-next-step-button")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".payment-info-next-step-button"))).click()

        # Click on the 'Confirm Order' button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".confirm-order-next-step-button")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".confirm-order-next-step-button"))).click()

        # Optionally, you can add assertions to verify the completion of the order process
        assert "https://demowebshop.tricentis.com/onepagecheckout" in driver.current_url


