import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class TestEshop:

    def test_add_to_cart(self, driver_setup):

        # Navigate to a product page (you can replace the URL with the desired product)
        driver_setup.driver.get("https://demowebshop.tricentis.com/build-your-own-expensive-computer")

        # Click the "Add to cart" button
        add_to_cart_button = driver_setup.driver.find_element(By.ID, "add-to-cart-button-19")
        add_to_cart_button.click()

        # Wait for the success message to appear (you might want to enhance this part based on the actual behavior of the website)
        time.sleep(3)

        # Verify that the item is added to the cart
        cart_icon = driver_setup.driver.find_element(By.CSS_SELECTOR, ".cart-qty")
        assert int(cart_icon.text) > 0, "Adding to cart failed"

        # Navigate to the shopping cart page
        driver_setup.driver.get("https://demowebshop.tricentis.com/cart")

        # Verify that the added item is in the shopping cart
        cart_items = driver_setup.driver.find_elements(By.CSS_SELECTOR, ".cart .product")
        assert len(cart_items) > 0, "Item not found in the shopping cart"

        # Close the browser
        driver_setup.driver.quit()


    def test_add_to_wishlist(self,driver_setup):
        # Set up the Chrome WebDriver
        driver = webdriver.Chrome()

        # Navigate to a product page (you can replace the URL with the desired product)
        driver.get("https://demowebshop.tricentis.com/build-your-own-expensive-computer")

        # Click the "Add to wishlist" button
        add_to_wishlist_button = driver.find_element(By.ID, "add-to-wishlist-button-19")
        add_to_wishlist_button.click()

        # Wait for the success message to appear (you might want to enhance this part based on the actual behavior of the website)
        time.sleep(3)

        # Verify that the success message is displayed
        success_message = driver.find_element(By.CSS_SELECTOR, ".bar-notification.success .content").text
        assert "The product has been added to your wishlist" in success_message, "Adding to wishlist failed"



