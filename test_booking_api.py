import requests

BASE_URL = "https://restful-booker.herokuapp.com"

def get_token():
    # This function gets an authentication token from the API.
    # We need this token for updating and deleting bookings (security reason).
    auth_payload = {
        "username": "admin",
        "password": "password123"
    }
    print("\n===== [API TEST] Requesting Auth Token =====")
    res = requests.post(f"{BASE_URL}/auth", json=auth_payload)
    print(f"Token status code: {res.status_code}")
    print("Token response JSON:", res.json())
    assert res.status_code == 200
    return res.json()["token"]

def test_create_booking():
    # This test creates a new booking with fixed data.
    # It then checks the status code and main fields in the response.
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
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    print(f"Create status code: {response.status_code}")
    print("Create response JSON:", response.json())
    assert response.status_code == 200
    booking = response.json()
    print("Booking ID:", booking.get("bookingid"))
    print("Firstname in response:", booking["booking"]["firstname"])
    # Make sure "bookingid" is returned and the firstname is correct
    assert "bookingid" in booking
    assert booking["booking"]["firstname"] == "Jim"

def test_get_booking_by_id():
    # This test creates a new booking first (so the ID exists!).
    # Then it fetches the booking by ID and checks the data.
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
    create_resp = requests.post(f"{BASE_URL}/booking", json=payload)
    print(f"Create status code: {create_resp.status_code}")
    print("Create response JSON:", create_resp.json())
    booking_id = create_resp.json()["bookingid"]
    print(f"Booking ID to fetch: {booking_id}")

    # Now try to GET the booking by its ID
    print(f"===== [API TEST] Fetching booking with ID {booking_id} =====")
    get_resp = requests.get(f"{BASE_URL}/booking/{booking_id}")
    print(f"GET status code: {get_resp.status_code}")
    print("GET response JSON:", get_resp.json())
    assert get_resp.status_code == 200
    booking = get_resp.json()
    print("Firstname fetched:", booking["firstname"])
    assert booking["firstname"] == "Jim"

def test_update_booking():
    # First, create a booking so you know the booking_id exists.
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
    print("\n===== [API TEST] Creating booking for UPDATE test =====")
    create_resp = requests.post(f"{BASE_URL}/booking", json=payload)
    print(f"Create status code: {create_resp.status_code}")
    print("Create response JSON:", create_resp.json())
    booking_id = create_resp.json()["bookingid"]
    print(f"Booking ID to update: {booking_id}")

    # Get a token, so you are authorized to update
    token = get_token()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}"
    }
    # Prepare new data to update the booking
    updated_payload = {
        "firstname": "Oren",
        "lastname": "Cohen",
        "totalprice": 200,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2023-02-01",
            "checkout": "2023-02-02"
        },
        "additionalneeds": "Lunch"
    }
    print(f"===== [API TEST] Updating booking ID {booking_id} =====")
    update_resp = requests.put(
        f"{BASE_URL}/booking/{booking_id}",
        json=updated_payload,
        headers=headers
    )
    print(f"Update status code: {update_resp.status_code}")
    print("Update response JSON:", update_resp.json())
    assert update_resp.status_code == 200
    updated = update_resp.json()
    print("Firstname after update:", updated["firstname"])
    assert updated["firstname"] == "Oren"

def test_delete_booking():
    # Again, first create a booking so you know what to delete.
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
    print("\n===== [API TEST] Creating booking for DELETE test =====")
    create_resp = requests.post(f"{BASE_URL}/booking", json=payload)
    print(f"Create status code: {create_resp.status_code}")
    print("Create response JSON:", create_resp.json())
    booking_id = create_resp.json()["bookingid"]
    print(f"Booking ID to delete: {booking_id}")

    # Get token for authentication
    token = get_token()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}"
    }
    # Send DELETE request
    print(f"===== [API TEST] Deleting booking ID {booking_id} =====")
    delete_resp = requests.delete(
        f"{BASE_URL}/booking/{booking_id}",
        headers=headers
    )
    print(f"Delete status code: {delete_resp.status_code}")

    # Check that it's really deleted (should be 404 now)
    print(f"===== [API TEST] Verifying booking ID {booking_id} is deleted =====")
    get_resp = requests.get(f"{BASE_URL}/booking/{booking_id}")
    print(f"GET after delete status code: {get_resp.status_code}")

    assert delete_resp.status_code == 201
    assert get_resp.status_code == 404
