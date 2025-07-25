from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

def setup_driver():
    options = Options()
    options.headless = True
    service = Service(executable_path='chromedriver')  # Ensure chromedriver is in your PATH
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def take_screenshot(driver, file_path):
    driver.save_screenshot(file_path)

def main():
    driver = setup_driver()
    try:
        # Load the registration page
        driver.get("http://localhost:8000/accounts/register/")
        
        # Take a screenshot before interacting with the form
        os.makedirs("screenshots", exist_ok=True)
        screenshot_before = "screenshots/before_register.png"
        take_screenshot(driver, screenshot_before)

        # Fill in the registration form
        driver.find_element(By.XPATH, '//*[@id="id_username"]').send_keys("testuser")
        driver.find_element(By.XPATH, '//*[@id="id_email"]').send_keys("testuser@example.com")
        driver.find_element(By.XPATH, '//*[@id="id_password1"]').send_keys("securepassword")
        driver.find_element(By.XPATH, '//*[@id="id_password2"]').send_keys("securepassword")

        # Submit the registration form
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Wait for 3 seconds after submission
        time.sleep(3)

        # Take a screenshot after submission
        screenshot_after = "screenshots/after_register.png"
        take_screenshot(driver, screenshot_after)

        # Print screenshot file paths and the first 300 characters of the final HTML
        print(f"Before Registration Screenshot: {screenshot_before}")
        print(f"After Registration Screenshot: {screenshot_after}")

        final_html = driver.page_source
        print(final_html[:300])

    finally:
        driver.quit()

if __name__ == "__main__":
    main()