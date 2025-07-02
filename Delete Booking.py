import requests

BASE_URL = "https://restful-booker.herokuapp.com"

def get_token():
    # This function requests an authentication token so we can delete bookings.
    auth_payload = {
        "username": "admin",
        "password": "password123"
    }
    print("\n===== [API TEST] Requesting Auth Token for Delete =====")
    res = requests.post(f"{BASE_URL}/auth", json=auth_payload)
    print(f"Token status code: {res.status_code}")
    print("Token response JSON:", res.json())
    assert res.status_code == 200  # Make sure we got a token successfully.
    return res.json()["token"]     # Return the token string.

def test_delete_booking():
    # Step 1: Create a booking to delete (so the test is always independent).
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
    # We get the ID of the booking we just created.
    booking_id = create_resp.json()["bookingid"]
    print(f"Booking ID to delete: {booking_id}")

    # Step 2: Get a token so we are allowed to delete.
    token = get_token()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}"
    }

    # Step 3: Send the delete request.
    print(f"===== [API TEST] Deleting booking ID {booking_id} =====")
    delete_resp = requests.delete(
        f"{BASE_URL}/booking/{booking_id}",
        headers=headers
    )
    print(f"Delete status code: {delete_resp.status_code}")

    # Step 4: Make sure the booking is actually deleted (should return 404).
    print(f"===== [API TEST] Verifying booking ID {booking_id} is deleted =====")
    get_resp = requests.get(f"{BASE_URL}/booking/{booking_id}")
    print(f"GET after delete status code: {get_resp.status_code}")

    # Check for correct status codes: 201 for delete, 404 when getting after delete.
    assert delete_resp.status_code == 201
    assert get_resp.status_code == 404
