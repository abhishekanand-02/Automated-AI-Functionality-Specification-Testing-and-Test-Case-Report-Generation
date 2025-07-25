import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
service = Service('/path/to/chromedriver')  # Update with your path to chromedriver

def main():
    driver = webdriver.Chrome(service=service, options=options)
    try:
        # Load the polls list page
        driver.get("http://localhost:8000/polls/list/")

        # Take a screenshot before interacting with the form
        os.makedirs('screenshots', exist_ok=True)
        driver.save_screenshot('screenshots/before_polls_list.png')

        # Fill in the form fields with test data
        username_field = driver.find_element(By.XPATH, '//*[@id="username"]')
        password_field = driver.find_element(By.XPATH, '//*[@name="password"]')
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        username_field.send_keys("testuser")
        password_field.send_keys("password123")

        # Submit the form
        submit_button.click()

        # Wait for 3 seconds after submission
        time.sleep(3)

        # Take a screenshot after submission
        driver.save_screenshot('screenshots/after_polls_list.png')

        # Print paths and final HTML content
        print('screenshots/before_polls_list.png')
        print('screenshots/after_polls_list.png')
        print(driver.page_source[:300])

    finally:
        driver.quit()

if __name__ == "__main__":
    main()