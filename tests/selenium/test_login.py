from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

if __name__ == "__main__":
    options = Options()
    options.headless = True
    service = Service('./chromedriver')  # Update the path to your ChromeDriver if necessary

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("http://localhost:8000/accounts/login/")
        
        # Take a screenshot before interacting with the form
        os.makedirs('screenshots', exist_ok=True)
        driver.save_screenshot('screenshots/before_login.png')

        # Fill in the form fields
        username_field = driver.find_element(By.XPATH, '//input[@name="username"]')
        password_field = driver.find_element(By.XPATH, '//input[@name="password"]')
        
        username_field.send_keys("testuser")
        password_field.send_keys("testpassword")

        # Submit the form
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()

        # Wait for 3 seconds after submission
        time.sleep(3)

        # Take a screenshot after submission
        driver.save_screenshot('screenshots/after_login.png')

        # Output screenshot paths and first 300 characters of final HTML
        print('Screenshots:')
        print('Before login: screenshots/before_login.png')
        print('After login: screenshots/after_login.png')

        print('Final HTML content:')
        print(driver.page_source[:300])

    finally:
        driver.quit()