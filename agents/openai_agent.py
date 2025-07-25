import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_functional_spec(source_code: str) -> str:
    prompt = f"""
    Analyze the Django source code below and generate a markdown document named 'functional_specifications.md'.
    It should include:
    1. User Interaction Flows
    2. URL Endpoints and their Purpose

    ```python
    {source_code}
    ```
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

def generate_selenium_test(source_code: str, spec: str, url: str) -> str:
    prompt = f"""
    Create a Selenium test in Python for the following URL: {url}.
    Use the context from source code and spec:

    SOURCE:
    ```python
    {source_code}
    ```

    SPEC:
    ```markdown
    {spec}
    ```
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
