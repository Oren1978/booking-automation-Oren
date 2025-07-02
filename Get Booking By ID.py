import requests

# The main API address.
BASE_URL = "https://restful-booker.herokuapp.com"

def test_get_booking_by_id():
    # This is the data we send to create a booking.
    payload = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-01-01",
            "checkout": "2023-01-02"
        },
        "additionalneeds": "Breakfast"
    }

    print("\n===== [API TEST] Creating booking for GET test =====")
    # First, create a new booking to get a valid ID.
    create_resp = requests.post(f"{BASE_URL}/booking", json=payload)
    print(f"Create status code: {create_resp.status_code}")
    print("Create response JSON:", create_resp.json())
    # Get the ID of the booking we just created.
    booking_id = create_resp.json()["bookingid"]
    print(f"Booking ID to fetch: {booking_id}")

    print(f"===== [API TEST] Fetching booking with ID {booking_id} =====")
    # Now, fetch the booking using the ID.
    get_resp = requests.get(f"{BASE_URL}/booking/{booking_id}")
    print(f"GET status code: {get_resp.status_code}")
    print("GET response JSON:", get_resp.json())

    # Make sure the GET request was successful.
    assert get_resp.status_code == 200
    booking = get_resp.json()
    # Print the names we got, and check them.
    print("Firstname fetched:", booking["firstname"])
    print("Lastname fetched:", booking["lastname"])
    # Check that the booking details match what we created.
    assert booking["firstname"] == "Jim"
    assert booking["lastname"] == "Brown"
