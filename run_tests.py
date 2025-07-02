import os

# This list holds all your available test scripts.
# Each tuple has a description and the shell command to run.
options = [
    ('Create Booking - API',      'pytest -s "Create Booking.py"'),
    ('Get Booking By ID - API',   'pytest -s "Get Booking By ID.py"'),
    ('All Bookings - API',        'pytest -s "test_booking_api.py"'),
    ('Delete Booking - API',      'pytest -s "Delete Booking.py"'),
    ('Update Booking - API',      'pytest -s "Update Booking.py"'),
    ('Full Room Lifecycle - UI',  'pytest -s "Full_room_lifecycle_test.py"'),
    ('UI Add Room - UI',          'pytest -s "UI - Adding new Room.py"'),
    ('UI Update Room - UI',       'pytest -s "UI - Updating My Room.py"'),
    ('UI Delete Room - UI',       'pytest -s "UI - Delete Room.py"'),
]

# Show the user the list of tests
print("\nAvailable tests:")
for idx, (desc, _) in enumerate(options, 1):
    print(f"{idx}. {desc}")

# Ask the user which test(s) to run (they can pick several, comma-separated)
choice = input("\nEnter the number of the test you want to run (or several, comma separated): ").strip()

# For each test number chosen, run the test using os.system (so it will run in the shell)
for ch in choice.split(","):
    try:
        i = int(ch) - 1
        if 0 <= i < len(options):
            print(f"\n--- Running: {options[i][0]} ---\n")
            os.system(options[i][1])
        else:
            print(f"Invalid choice: {ch}")
    except ValueError:
        print(f"Invalid input: {ch}")
