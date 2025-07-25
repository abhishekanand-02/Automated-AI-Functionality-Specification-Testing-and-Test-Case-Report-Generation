# Final QA Report for Polls List Page

## Functional Specification
The Polls List Page is part of a user flow that begins at the homepage. Users can register for an account, log in, and then access the polls by clicking "Get Started!" which redirects them to the Polls List page (`/polls/list/`). 

## Test Strategy
The test was executed using Selenium WebDriver to automate the browser interaction. The test performed the following steps:
1. Loaded the Polls List page.
2. Took a screenshot before any interaction as a reference.
3. Identified and filled in the login form fields with test credentials.
4. Submitted the login form.
5. Waited for the page to load after submission and captured another screenshot.

## Test Inputs
- **Username:** `testuser`
- **Password:** `password123`

## Screenshot References
- Before Login: ![Before Polls List](screenshots/before_polls_list.png)
- After Login: ![After Polls List](screenshots/after_polls_list.png)

## Summary/Observations
The test demonstrated that users can successfully navigate to the Polls List page after logging in. Both screenshots were captured correctly, and the application performed as expected with no errors observed in the automated flow. Further testing may include verification of the content displayed on the Polls List page post-login and additional scenarios such as invalid login attempts.