import random
from playwright.sync_api import sync_playwright

def test_update_room_from_file_card():
    # Read the last created room number from a file, so we can update that room
    with open("last_room.txt", "r") as f:
        room_num = f.read().strip()
    print(f"Updating room {room_num}")

    with sync_playwright() as p:
        # Open the browser and go to the rooms admin page
        browser = p.chromium.launch(headless=False, slow_mo=350)
        page = browser.new_page()
        page.goto("https://automationintesting.online/admin/rooms")

        # --- Login section ---
        page.fill('input[placeholder="Enter username"]', "admin")
        page.fill('input[placeholder="Password"]', "password")
        page.click('button:has-text("Login")')
        page.wait_for_selector('text=Logout')
        print("Login successful.")

        # --- Wait for the room card to appear (room number from file) ---
        page.wait_for_selector(f"text={room_num}", timeout=6000)

        # Find the room card and click on it
        room_card = page.locator(f"text={room_num}")
        assert room_card.is_visible()
        room_card.click()
        print(f"Entered room {room_num} card page.")

        # Make sure we see the Edit button and click it
        page.wait_for_selector('button:has-text("Edit")')
        page.click('button:has-text("Edit")')
        print("Clicked Edit.")

        # Try to wait for a specific checkbox (sometimes they load late)
        try:
            page.wait_for_selector("#refreshCheckbox", timeout=3000)
        except Exception:
            print("Checkboxes may not be visible or exist!")

        # --- Choose new random values for the room (for update) ---
        # NOTE: The room number itself is NOT changed, only the other properties
        new_price = str(random.randint(1, 999))
        new_type = random.choice(["Single", "Twin", "Double", "Family", "Suite"])
        new_accessible = random.choice(["true", "false"])
        new_description = "This room updated by Playwright E2E"
        new_image = "https://www.mwtestconsultancy.co.uk/img/room2.jpg"

        # Do NOT touch the room name, only update type, accessibility, price
        page.select_option("#type", label=new_type)
        page.select_option("#accessible", label=new_accessible)
        page.fill("#roomPrice", new_price)

        # --- Update features: randomly select which checkboxes to check/uncheck ---
        features = [
            "#wifiCheckbox", "#tvCheckbox", "#radioCheckbox",
            "#refreshCheckbox", "#safeCheckbox", "#viewsCheckbox"
        ]
        new_features = random.sample(features, k=random.randint(1, len(features)))
        for selector in features:
            try:
                if page.locator(selector).is_visible():
                    if selector in new_features:
                        page.check(selector)
                    else:
                        page.uncheck(selector)
            except Exception as e:
                print(f"Checkbox {selector} not found or not interactable: {e}")

        # Update the description and image fields too
        page.fill("#description", new_description)
        page.fill("#image", new_image)

        print(f"Updating room fields: type={new_type}, accessible={new_accessible}, price={new_price}, features={new_features}, description={new_description}")

        # Click the Update button to save changes
        page.click("#update")
        print("Clicked Update.")

        # Wait a little and verify the room still appears in the system
        page.wait_for_timeout(1500)
        page.goto("https://automationintesting.online/admin/rooms")
        page.wait_for_selector('text=Logout', timeout=6000)
        page.wait_for_selector(f"text={room_num}", timeout=6000)
        assert page.is_visible(f"text={room_num}")
        print(f"Room {room_num} updated successfully.")

        # Close the browser at the end
        browser.close()
