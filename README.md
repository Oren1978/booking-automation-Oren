**Booking Platform Test Suite**

**Overview**

Automated tests (UI and API) for the Restful Booker Platform Demo project can be found in this repository. End-to-end scenarios, room management, and booking operations are the focus of the tests, which cover the main room booking workflows through UI and API endpoints.

The suite is implemented in Python using the Playwright library for UI tests and test for test orchestration. To save time, all test cases can be executed using a single CLI menu.

**Repository Structure**

├── **Full_room_lifecycle_test.py** # End-to-end UI test: create, update, delete room

├── **test_booking_api.py** # API tests for booking create, retrieve, update, delete

├── **Create Booking.py** # Standalone test: create booking (API)

├── **Get Booking By ID.py** # Standalone test: get booking by ID (API)

├── **Update Booking.py** # Standalone test: update booking (API)

├── **Delete Booking.py** # Standalone test: delete booking (API)

├── **UI - Adding new Room.py** # Standalone test: add new room (UI)

├── **UI - Updating My Room.py** # Standalone test: update room (UI)

├── **UI - Delete Room.py** # Standalone test: delete room (UI)

├── **run_tests.py** # CLI runner script for all test suites

└── **README.md** # Documentation (this file)

**How to Run**

**Prerequisites**

- Python 3.8+ (tested up to 3.13)
- Playwright (install with pip install playwright)
- Install browser drivers for Playwright:

playwright install

- [pytest](https://pytest.org/) (install with pip install pytest)
- Clone the repository
- Install dependencies:

_pip install -r requirements.txt_

- Run all tests with output: **pytest -s**

**Test Scenarios Covered**

- Create Booking (POST /booking)
- Get Booking By ID (GET /booking/{id})
- Update Booking (PUT /booking/{id})
- Delete Booking (DELETE /booking/{id})

**Running the Tests**

You can run any individual test using:

pytest -s "test_file.py" (Use any individual test from above list)

**Or, to launch an interactive CLI menu and choose the tests you want to run:**

_python run_tests.py_

- Select one or more tests by entering their number(s), comma-separated (e.g., 2,3,6).
- The output will be printed to the terminal.

**Test Descriptions**

| **Test File** | **Description** |
| --- | --- |
| Full_room_lifecycle_test.py | Full UI flow: create, update, delete a room in one scenario |
| UI - Adding new Room.py | Standalone: create a new room (UI) |
| UI - Updating My Room.py | Standalone: update an existing room (UI) |
| UI - Delete Room.py | Standalone: delete an existing room (UI) |
| test_booking_api.py | API tests: create, read, update, delete bookings |
| Create Booking.py | Standalone: create booking (API) |
| Get Booking By ID.py | Standalone: retrieve booking by ID (API) |
| Update Booking.py | Standalone: update booking (API) |
| Delete Booking.py | Standalone: delete booking (API) |
| run_tests.py | CLI menu for running any/all the tests above |

**Noteworthy Decisions and Known Issues**

- **UI Selector Strategy:**  
    UI tests rely on visible data-testid attributes and form field selectors for robust automation.  
    Room deletion uses detection of .roomDelete buttons inside each room's div.
- **Data Management:**  
    Temporary files (e.g., last_room.txt) are used to persist the last-created room number for update/delete flows.  
    Each full room lifecycle test ensures that the room is removed from the system at the end of the run.
- **Determinism:**  
    After running the lifecycle or delete tests, the test room is verified as **not present** in the system.
- **Bugs/Quirks Observed:**
  - UI page loads sometimes require extra wait/sleep time for consistent runs.  
        Extra waits were added to improve stability.
  - Deleting a room via UI sometimes requires focusing the correct room card; deletion is always verified.
- **Playwright Browsers:**  
    All UI tests launch browsers in **headed mode** (headless=False) with slow motion for demonstration.
- **Authentication:**  
    All UI and API tests use demo admin credentials (admin / password) as required by the app.

**How to Add More Tests**

- Place new test scripts in the root directory, following the naming conventions.
- Add the test's CLI command to run_tests.py for menu integration.

**Example: Run the Full Lifecycle UI Test**

_python run_tests.py_

\# Choose: "Full Room Lifecycle"

- This will create a room, update it, and delete it, with waits between each step for easy UI observation.

**Contact**

For questions, issues, or suggestions, please contact the repository maintainer.