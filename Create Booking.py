import requests

# This is the base URL for the API.
BASE_URL = "https://restful-booker.herokuapp.com"

def test_create_booking():
    # This is the data we will send to create a new booking (the payload).
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

    print("\n===== [API TEST] Creating new booking =====")
    # Here we send a POST request to create a booking.
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    print(f"Status code: {response.status_code}")
    print("Response JSON:", response.json())

    # Make sure the response is OK (HTTP 200 means success).
    assert response.status_code == 200, "Status code is not 200"

    booking = response.json()
    # Print the booking ID and check some fields in the response.
    print("Booking ID:", booking.get("bookingid"))
    print("Firstname in response:", booking["booking"]["firstname"])
    print("Lastname in response:", booking["booking"]["lastname"])

    # Check that the response has a bookingid (very important!).
    assert "bookingid" in booking, "bookingid is missing"
    # Check that the firstname and lastname match what we sent.
    assert booking["booking"]["firstname"] == "Jim"
    assert booking["booking"]["lastname"] == "Brown"
