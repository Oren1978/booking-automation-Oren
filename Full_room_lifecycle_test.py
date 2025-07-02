import random
import time
from playwright.sync_api import sync_playwright

def test_full_room_lifecycle():
    # This function tests the full lifecycle of a hotel room: create, update, then delete.

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=250)
        page = browser.new_page()
        page.goto("https://automationintesting.online/admin")

        # --- Login Step ---
        # Login as admin using UI.
        page.fill('input[placeholder="Enter username"]', "admin")
        page.fill('input[placeholder="Password"]', "password")
        page.click('button:has-text("Login")')
        page.wait_for_selector('text=Logout')
        print("Login successful.")
        time.sleep(1)

        # --- Add Room Step ---
        # Create a new room with random details
        room_num = str(random.randint(1000, 9999))
        room_types = ["Single", "Twin", "Double", "Family", "Suite"]
        type_choice = random.choice(room_types)
        accessible_choice = random.choice(["true", "false"])
        price = str(random.randint(100, 999))
        features = [
            ("WiFi", "#wifiCheckbox"),
            ("TV", "#tvCheckbox"),
            ("Radio", "#radioCheckbox"),
            ("Refreshments", "#refreshCheckbox"),
            ("Safe", "#safeCheckbox"),
            ("Views", "#viewsCheckbox"),
        ]
        # Choose a random set of features
        chosen_features = random.sample(features, k=random.randint(1, len(features)))
        page.fill("[data-testid='roomName']", room_num)
        page.select_option("#type", label=type_choice)
        page.select_option("#accessible", label=accessible_choice)
        page.fill("#roomPrice", price)
        # Set each feature's checkbox according to selection
        for label, selector in features:
            if (label, selector) in chosen_features:
                page.check(selector)
            else:
                page.uncheck(selector)
        page.click("#createRoom")
        print(f"Room {room_num} added.")
        page.wait_for_selector(f"text={room_num}", timeout=6000)
        assert page.is_visible(f"text={room_num}")
        time.sleep(5)  # Wait a few seconds before updating

        # --- Update Room Step ---
        # Go to rooms page, find our room, and edit it
        page.goto("https://automationintesting.online/admin/rooms")
        page.wait_for_selector(f"text={room_num}", timeout=6000)
        room_card = page.locator(f"text={room_num}")
        assert room_card.is_visible()
        room_card.click()
        page.wait_for_selector('button:has-text("Edit")')
        page.click('button:has-text("Edit")')
        time.sleep(1)
        new_price = str(random.randint(1, 999))
        new_type = random.choice(room_types)
        new_accessible = random.choice(["true", "false"])
        new_description = "Updated by Playwright E2E"
        new_image = "https://www.mwtestconsultancy.co.uk/img/room2.jpg"
        # Choose random features again for update
        new_features = random.sample([x[1] for x in features], k=random.randint(1, len(features)))
        page.select_option("#type", label=new_type)
        page.select_option("#accessible", label=new_accessible)
        page.fill("#roomPrice", new_price)
        for selector in [x[1] for x in features]:
            try:
                # Check or uncheck features based on new selection
                if page.locator(selector).is_visible():
                    if selector in new_features:
                        page.check(selector)
                    else:
                        page.uncheck(selector)
            except Exception as e:
                print(f"Checkbox {selector} not found or not interactable: {e}")
        page.fill("#description", new_description)
        page.fill("#image", new_image)
        print(f"Updating room fields: type={new_type}, accessible={new_accessible}, price={new_price}, features={new_features}, description={new_description}")
        page.click("#update")
        print("Clicked Update.")
        page.wait_for_timeout(1500)
        # Go back to rooms page and check room still exists
        page.goto("https://automationintesting.online/admin/rooms")
        page.wait_for_selector('text=Logout', timeout=6000)
        page.wait_for_selector(f"text={room_num}", timeout=6000)
        assert page.is_visible(f"text={room_num}")
        print(f"Room {room_num} updated successfully.")
        time.sleep(5)  # Wait a few seconds before deleting

        # --- Delete Room Step ---
        # Go again to rooms page and delete the room by clicking the "X"
        page.goto("https://automationintesting.online/admin/rooms")
        page.wait_for_selector(f"text={room_num}", timeout=6000)
        room_divs = page.locator('div[data-testid="roomlisting"]')
        found = False
        for i in range(room_divs.count()):
            div = room_divs.nth(i)
            if room_num in div.inner_text():
                del_btn = div.locator('span.roomDelete')
                assert del_btn.is_visible(), f"Delete button not visible in room {room_num}"
                del_btn.click()
                print(f"Clicked delete for room {room_num}")
                found = True
                time.sleep(1)
                break

        assert found, f"Room {room_num} not found in any roomlisting div!"

        # Make sure the room is not visible anymore
        time.sleep(1)
        assert not page.is_visible(f"text={room_num}"), f"Room {room_num} still visible after delete!"
        print(f"Room {room_num} deleted successfully.")

        # Close the browser at the end of the test
        browser.close()
