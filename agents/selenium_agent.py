from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def run_test_with_screenshot(url: str, test_code: str, screenshot_path: str):
    with open("temp_test.py", "w") as f:
        f.write(test_code)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)
    driver.save_screenshot(f"{screenshot_path}_before.png")

    exec(test_code, {"driver": driver})

    time.sleep(2)
    driver.save_screenshot(f"{screenshot_path}_after.png")
    driver.quit()
