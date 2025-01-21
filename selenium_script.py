from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os
import time
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', '/path/to/chromedriver')  # Use environment variable
SENDCLOUD_EMAIL = os.getenv('SENDCLOUD_EMAIL', 'your_email@example.com')
SENDCLOUD_PASSWORD = os.getenv('SENDCLOUD_PASSWORD', 'your_password')

# Initialize WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)
wait = WebDriverWait(driver, 15)

# Global variable for orders with errors
orders_with_errors = []

def login():
    """Logs in to the Sendcloud platform."""
    try:
        driver.get('https://account.sendcloud.com/login/')
        logging.info("Navigated to Sendcloud login page.")
        
        # Wait for email and password fields
        email_field = wait.until(EC.presence_of_element_located((By.NAME, 'login')))
        password_field = driver.find_element(By.NAME, 'password')
        
        # Enter credentials
        email_field.send_keys(SENDCLOUD_EMAIL)
        password_field.send_keys(SENDCLOUD_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        
        logging.info("Login submitted successfully.")
        time.sleep(5)
    except Exception as e:
        logging.error(f"Error during login: {e}")
        driver.quit()

def load_all_records():
    """Loads all records on the page using lazy scrolling."""
    try:
        # Open the date picker and select filter
        date_picker = driver.find_element(By.CSS_SELECTOR, '[data-test="date-picker-range-toggle"]')
        date_picker.click()
        driver.find_element(By.CSS_SELECTOR, '[data-test="date-picker-range-7days"]').click()
        logging.info("Selected 'Today' filter.")
        
        # Lazy load by scrolling
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        logging.info("All records loaded.")
    except Exception as e:
        logging.error(f"Error loading records: {e}")

def edit_order(order_card):
    """Edits a single order."""
    try:
        edit_button = order_card.find_element(By.CSS_SELECTOR, '[data-test="edit-order"]')
        edit_button.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="total-order-value-input"]')))
        logging.info("Edit modal opened successfully.")
        
        # Process and save changes (if required)
        # Additional logic for editing can be added here
        
        save_button = driver.find_element(By.CSS_SELECTOR, '[data-test="neov-save-button"]')
        save_button.click()
        logging.info("Order saved successfully.")
    except TimeoutException:
        logging.error("Timeout while editing order.")
    except Exception as e:
        logging.error(f"Error while editing order: {e}")

def store_orders_with_errors():
    """Saves the list of orders with errors to a JSON file."""
    try:
        file_path = 'orders_with_errors.json'
        with open(file_path, 'w') as file:
            json.dump(orders_with_errors, file, indent=4)
        logging.info(f"Orders with errors saved to {file_path}.")
    except Exception as e:
        logging.error(f"Error saving orders: {e}")

def main():
    """Main function to run the script."""
    try:
        login()
        load_all_records()
        # Add logic to process all orders here
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        driver.quit()
        logging.info("Browser closed.")

if __name__ == "__main__":
    main()

