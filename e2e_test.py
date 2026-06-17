import requests
import time

BASE_URL = "http://127.0.0.1:5000/api"

def print_result(step_name, response):
    try:
        print(f"[{step_name}] Status: {response.status_code} - Body: {response.json()}")
    except Exception as e:
        print(f"[{step_name}] Status: {response.status_code} - Text: {response.text}")

def run_tests():
    print("--- STARTING E2E EXHAUSTIVE TEST ---")
    
    # 1. Register a normal user
    timestamp = int(time.time())
    username = f"user_{timestamp}"
    email = f"user_{timestamp}@test.com"
    
    print("\n--- USER FLOW ---")
    resp = requests.post(f"{BASE_URL}/auth/signup", json={
        "username": username,
        "email": email,
        "password": "Password123!",
        "confirm_password": "Password123!",
        "role": "member"
    })
    print_result("Register User", resp)
    
    # 2. Login as the normal user
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "username": username,
        "password": "Password123!"
    })
    print_result("Login User", resp)
    
    # 3. Get spaces
    resp = requests.get(f"{BASE_URL}/spaces")
    print_result("Get Spaces", resp)
    spaces_data = []
    if resp.status_code == 200:
        spaces_data = resp.json().get("data", [])
    
    # 4. Create a booking
    space_name = spaces_data[0]["name"] if spaces_data else "Oficina 1"
    resp = requests.post(f"{BASE_URL}/bookings", json={
        "username": username,
        "space_name": space_name,
        "booking_date": "2026-06-15",
        "booking_time": "10:00"
    })
    print_result("Create Booking", resp)
    booking_id = None
    if resp.status_code == 201:
        booking_data = resp.json().get("data", {})
        if isinstance(booking_data, dict):
            booking_id = booking_data.get("id")
        elif isinstance(booking_data, list) and len(booking_data) > 0:
            booking_id = booking_data[0].get("id")
            
    # 5. Get user bookings
    resp = requests.get(f"{BASE_URL}/bookings?username={username}")
    print_result("Get User Bookings", resp)
    
    print("\n--- ADMIN FLOW ---")
    # 6. Admin should ideally be logged in but the API might not be validating roles
    # Let's test if we can get all users
    resp = requests.get(f"{BASE_URL}/users")
    print_result("Get All Users (Admin)", resp)
    
    # 7. Create a Space (Admin)
    resp = requests.post(f"{BASE_URL}/spaces", json={
        "name": f"Nuevo Espacio {timestamp}",
        "type": "sala_reuniones",
        "capacity": 10,
        "price": 5000
    })
    print_result("Create Space (Admin)", resp)
    space_id = None
    if resp.status_code == 201:
        s_data = resp.json().get("data", {})
        if isinstance(s_data, list) and len(s_data) > 0:
            space_id = s_data[0].get("id")
        elif isinstance(s_data, dict):
            space_id = s_data.get("id")

    # 8. Approve Booking (Admin)
    if booking_id:
        resp = requests.patch(f"{BASE_URL}/bookings/{booking_id}", json={
            "status": "aprobada"
        })
        print_result("Approve Booking", resp)
    else:
        print("[Approve Booking] Skipped, no booking_id")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"Error executing tests: {e}")
