import os
import requests
import openai
import logging
from dotenv import load_dotenv
from logger import logging
from pathlib import Path

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
BASE_DIR = Path(__file__).resolve().parent.parent


def fetch_source_from_localhost(url="http://localhost:8000"):
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f"Fetched source from {url}")
        return response.text
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return ""


def get_functional_spec_from_html(html_source):
    if not html_source:
        logging.warning("No HTML source to analyze.")
        return "No HTML source to analyze."

    prompt = f"""
        You're a senior software architect.

        From the HTML source of a Django-based homepage provided below, generate a clear and concise **functional specification** in Markdown format.

        Your output must contain ONLY the following sections in this order:

        ## User Interaction Flows
        - Describe the user's journey in exactly 4-6 short steps.
        - Start from homepage → register → login → and so on.
        - Include the route (`/path/`) in backticks inside each step.

        ## URL Endpoints and their Purpose
        - List each endpoint in the order it appears in the user flow.
        - Use this exact format:
          **Name (`/url/`)** — one-line purpose of that endpoint.

        Be direct and simple. Avoid repeating "Navigation", "Interface", or "Page" unless necessary. Avoid generic headings like "Navigation Bar Access".

        HTML Source:
        {html_source}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in UX analysis and functional spec writing."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f" Error from OpenAI: {e}"


def save_spec_to_markdown(spec_text, output_file=None):
    if output_file is None:
        output_file = BASE_DIR / "outputs" / "functional_specifications.md"
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(spec_text)
    
    logging.info(f"Functional spec saved to {output_file}")

# if __name__ == "__main__":
#     html = fetch_source_from_localhost()
#     spec = get_functional_spec_from_html(html)
#     save_spec_to_markdown(spec)
