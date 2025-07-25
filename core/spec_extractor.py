import os
import re
import requests
import openai
from dotenv import load_dotenv
from pathlib import Path 

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_SPEC = BASE_DIR / "outputs" / "functional_specifications.md"
TESTS_OUTPUT_DIR = BASE_DIR / "tests" / "selenium"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
BASE_URL = "http://localhost:8000"

os.makedirs(TESTS_OUTPUT_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def extract_routes_from_markdown(md_path):
    routes = []
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"\*\*(.*?) \(`/([^`]+)`\)"
    matches = re.findall(pattern, content)
    for name, path in matches:
        routes.append((name.strip().lower().replace(" ", "_"), f"/{path.strip()}"))
    return routes


def fetch_html_from_url(path):
    url = f"{BASE_URL}{path}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"[✓] Fetched {url}")
        return response.text
    except requests.RequestException as e:
        print(f"[✗] Failed to fetch {url}: {e}")
        return None


def get_selenium_test_from_html(html_content, page_name, path):
    screenshot_before_path = str(SCREENSHOTS_DIR / f"before_{page_name}.png").replace('\\', '/')
    screenshot_after_path = str(SCREENSHOTS_DIR / f"after_{page_name}.png").replace('\\', '/')

    prompt = f"""
        You are a senior QA automation engineer.

        Write a standalone Python script using Selenium (not pytest) to test the `{page_name}` page of a Django web application.

        Requirements:
        - Use `webdriver.Chrome(options=options)` to set headless mode using `Options()` (not `chrome_options`)
        - Use modern Selenium 4 syntax: `driver.find_element(By.XPATH, '...')`
        - Load the page from: http://localhost:8000{path}
        - Take a screenshot before interacting with the form and save it as: {screenshot_before_path}
        - Fill in the form fields with test data
        - Submit the form using the correct button
        - Wait for 3 seconds after submission
        - Take a screenshot after submission and save it as: {screenshot_after_path}
        - Print the screenshot file paths and the first 300 characters of the final HTML
        - Use a try-finally block to ensure `driver.quit()` is always called
        - Include all necessary imports
        - Wrap execution logic under: `if __name__ == "__main__"`
        - Output only valid Python code, no markdown or explanations
        - This is the page HTML content:
        {html_content}
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional QA automation engineer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[✗] OpenAI error for {path}: {e}")
        return None

def clean_gpt_generated_code(raw_code: str) -> str:
    raw_code = raw_code.strip()

    fenced_pattern = r"(?i)```(?:python)?\s*(.*?)```"
    match = re.search(fenced_pattern, raw_code, re.DOTALL)
    if match:
        return match.group(1).strip()

    if raw_code.lower().startswith("python\n"):
        return raw_code.split("\n", 1)[1].strip()

    return raw_code



def save_test_script(code, filename):
    cleaned_code = clean_gpt_generated_code(code)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(cleaned_code)
    print(f"[✓] Cleaned & saved script to {filename}")



# if __name__ == "__main__":
#     routes = extract_routes_from_markdown(INPUT_SPEC)

#     for name, path in routes:
#         html = fetch_html_from_url(path)
#         if not html:
#             continue

#         test_code = get_selenium_test_from_html(html, name, path)
#         if not test_code:
#             continue

#         save_test_script(test_code, os.path.join(TESTS_OUTPUT_DIR, f"test_{name}.py"))
