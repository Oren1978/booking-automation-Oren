import random
from playwright.sync_api import sync_playwright

def test_add_room_random_and_save():
    # This function creates a new hotel room with random data, then saves its number to a file for later use.
    with sync_playwright() as p:
        # Start a browser in non-headless mode with slow motion so you can see the steps
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        page.goto("https://automationintesting.online/admin")

        # --- Login step ---
        # Fill username and password fields and log in as admin
        page.fill('input[placeholder="Enter username"]', "admin")
        page.fill('input[placeholder="Password"]', "password")
        page.click('button:has-text("Login")')
        # Wait until "Logout" button appears to confirm login was successful
        page.wait_for_selector('text=Logout')
        print("Login successful.")

        # --- Generate random values for the new room ---
        # Room number, type, accessibility, price, and features are all randomized
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
        # Randomly select a subset of the features for this room
        chosen_features = random.sample(features, k=random.randint(1, len(features)))

        # --- Fill all fields for the room ---
        page.fill("[data-testid='roomName']", room_num)
        page.select_option("#type", label=type_choice)
        page.select_option("#accessible", label=accessible_choice)
        page.fill("#roomPrice", price)

        # Check or uncheck the features' checkboxes as needed
        for label, selector in features:
            if (label, selector) in chosen_features:
                page.check(selector)
            else:
                page.uncheck(selector)

        print(f"Room #: {room_num}, Type: {type_choice}, Accessible: {accessible_choice}, Price: {price}, Features: {[x[0] for x in chosen_features]}")

        # --- Click the "Create" button to add the room ---
        page.click("#createRoom")
        print("Clicked Create button.")

        # --- Verify the room was created and is visible in the UI ---
        page.wait_for_selector(f"text={room_num}", timeout=5000)
        assert page.is_visible(f"text={room_num}")
        print(f"Room {room_num} added successfully.")

        # --- Save the room number to a text file so it can be used by other tests ---
        with open("last_room.txt", "w") as f:
            f.write(room_num)
        print(f"Saved room number {room_num} to last_room.txt.")

        # --- End the test by closing the browser ---
        browser.close()
