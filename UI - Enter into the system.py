from playwright.sync_api import sync_playwright

def test_login_admin():
    # This function tests if you can log in as admin to the admin UI page

    with sync_playwright() as p:
        # Start a Chromium browser in visible mode with a slow motion so a human can see what happens
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.goto("https://automationintesting.online/admin")

        # Wait until the username input field appears (up to 10 seconds)
        page.wait_for_selector('input[placeholder="Enter username"]', timeout=10000)
        # Fill in username and password for the admin user
        page.fill('input[placeholder="Enter username"]', "admin")
        page.fill('input[placeholder="Password"]', "password")
        # Click the Login button
        page.click('button:has-text("Login")')

        # Wait for the Logout text to appear (means login was successful)
        page.wait_for_selector('text=Logout', timeout=10000)
        assert page.is_visible('text=Logout')
        # Print a message to confirm login worked
        print("Login successful, Logout button is visible.")

        # Close the browser
        browser.close()
