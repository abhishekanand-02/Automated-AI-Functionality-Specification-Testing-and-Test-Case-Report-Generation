import os
from pathlib import Path
import openai

def generate_llm_report(page_name):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(" OPENAI_API_KEY environment variable not set.")
        return

    base_dir = Path(__file__).resolve().parent.parent

    spec_path = base_dir / "outputs" / "functional_specifications.md"
    screenshot_before = base_dir / "screenshots" / f"before_{page_name}.png"
    screenshot_after = base_dir / "screenshots" / f"after_{page_name}.png"
    test_file = base_dir / "tests" / "selenium" / f"test_{page_name}.py"

    report_output = base_dir / "reports" / f"final_report_{page_name}.md"
    report_output.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(spec_path, "r") as f:
            spec_content = f.read()

        with open(test_file, "r") as f:
            test_code = f.read()

    except FileNotFoundError as e:
        print(f"Missing file: {e}")
        return

    prompt = f"""
        You are a QA lead. Using the following information, generate a clean, professional QA test report in Markdown format for the `{page_name}` page.
        
        ### Functional Specification:
        {spec_content}
        
        ### Selenium Test Code:
        {test_code}
        
        
        Screenshots:
        - Before: screenshots/before_{page_name}.png
        - After: screenshots/after_{page_name}.png
        
        Requirements:
        - Title: Final QA Report for {page_name} Page
        - Section for functional spec (briefly summarize)
        - Section for test strategy (based on the script)
        - Mention test inputs (e.g., username/password if used)
        - Screenshot references
        - Final summary/observations
        
        Output only valid Markdown.
"""

    try:
    
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional QA automation engineer."},
                {"role": "user", "content": prompt}
            ]
        )

        report_md = response.choices[0].message.content.strip()

        with open(report_output, "w") as f:
            f.write(report_md)

        print(f" Final LLM-generated report saved to: {report_output}")

    except Exception as e:
        print(f" OpenAI Error: {e}")


# if __name__ == "__main__":
#     generate_llm_report("register")
#     generate_llm_report("login")
#     generate_llm_report("polls_list")
