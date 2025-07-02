import time
from playwright.sync_api import sync_playwright

def test_delete_room():
    # Read the last created room number from a file, so we know which room to delete
    with open("last_room.txt", "r") as f:
        room_num = f.read().strip()
    print(f"Going to delete room {room_num}")

    with sync_playwright() as p:
        # Open the browser and go to the admin rooms page
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()
        page.goto("https://automationintesting.online/admin/rooms")

        # --- Login as admin ---
        page.fill('input[placeholder="Enter username"]', "admin")
        page.fill('input[placeholder="Password"]', "password")
        page.click('button:has-text("Login")')
        page.wait_for_selector('text=Logout')
        print("Login successful.")

        # --- Wait for the room to appear on the page ---
        page.wait_for_selector(f"text={room_num}", timeout=6000)

        # --- Find the room's DIV by checking all roomlisting elements ---
        room_divs = page.locator('div[data-testid="roomlisting"]')
        found = False
        for i in range(room_divs.count()):
            div = room_divs.nth(i)
            # Check if this div contains the room number
            if room_num in div.inner_text():
                # Found the correct room! Click the delete "X" button (span with class roomDelete)
                del_btn = div.locator('span.roomDelete')
                assert del_btn.is_visible(), f"Delete button not visible in room {room_num}"
                del_btn.click()
                print(f"Clicked delete for room {room_num}")
                found = True
                time.sleep(1)  # Wait a moment for the UI to update
                break

        # If we never found the room, fail the test!
        assert found, f"Room {room_num} not found in any roomlisting div!"

        # --- Make sure the room is actually gone (not visible on the page) ---
        time.sleep(1)
        assert not page.is_visible(f"text={room_num}"), f"Room {room_num} still visible after delete!"
        print(f"Room {room_num} deleted successfully.")

        # Close the browser
        browser.close()
