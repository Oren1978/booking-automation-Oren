import requests

# The base URL for the RESTful Booker API
BASE_URL = "https://restful-booker.herokuapp.com"

def get_token():
    # This function gets an authentication token from the API.
    auth_payload = {
        "username": "admin",
        "password": "password123"
    }
    print("\n===== [API TEST] Requesting Auth Token for Update =====")
    res = requests.post(f"{BASE_URL}/auth", json=auth_payload)
    print(f"Token status code: {res.status_code}")
    print("Token response JSON:", res.json())
    # We check if the token request was successful.
    assert res.status_code == 200
    # Return the token from the response.
    return res.json()["token"]

def test_update_booking():
    # 1. First, create a new booking to update later.
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
    # Save the ID of the booking we just created.
    booking_id = create_resp.json()["bookingid"]
    print(f"Booking ID to update: {booking_id}")

    # 2. Now, get an authentication token for the update.
    token = get_token()
    # This is the header needed to authorize the update request.
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}"
    }

    # 3. Prepare new details for updating the booking.
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
    # Now send the PUT request to update the booking.
    update_resp = requests.put(
        f"{BASE_URL}/booking/{booking_id}",
        json=updated_payload,
        headers=headers
    )
    print(f"Update status code: {update_resp.status_code}")
    print("Update response JSON:", update_resp.json())

    # Check if the update was successful.
    assert update_resp.status_code == 200
    updated = update_resp.json()
    # Print the updated details and check if they are correct.
    print("Firstname after update:", updated["firstname"])
    print("Lastname after update:", updated["lastname"])
    print("Totalprice after update:", updated["totalprice"])
    assert updated["firstname"] == "Oren"
    assert updated["lastname"] == "Cohen"
    assert updated["totalprice"] == 200
