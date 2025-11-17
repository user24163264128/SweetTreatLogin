import requests

BASE_URL = "http://127.0.0.1:8000"

# ----------------------------
# Helper
# ----------------------------
def print_section(title):
    print("\n" + "="*60)
    print(f">> {title}")
    print("="*60)

# ----------------------------
# 1. REGISTER USER
# ----------------------------
print_section("REGISTER USER")

register_payload = {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "password": "pass123",
    "role": "user"
}

r = requests.post(f"{BASE_URL}/auth/register", json=register_payload)
print("Status:", r.status_code)
try:
    print("Response:", r.json())
except:
    print("Raw response:", r.text)

# ----------------------------
# 2. LOGIN USER
# ----------------------------
print_section("LOGIN USER")

login_payload = {
    "username": "john@example.com",  # OAuth2 form expects username
    "password": "pass123"
}

r = requests.post(f"{BASE_URL}/auth/login", data=login_payload)
print("Status:", r.status_code)
try:
    print("Response:", r.json())
except:
    print("Raw response:", r.text)

access_token = None
refresh_cookie = None

if r.status_code == 200:
    access_token = r.json().get("access_token")
    refresh_cookie = r.cookies.get("refresh_token")
    print("Cookies after login:", r.cookies.get_dict())

# ----------------------------
# 3. ACCESS DASHBOARD
# ----------------------------
print_section("GET /dashboard/user")
headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
r = requests.get(f"{BASE_URL}/dashboard/user", headers=headers)
print("Status:", r.status_code)
try:
    print("Response:", r.json())
except:
    print("Raw response:", r.text)

# ----------------------------
# 4. REFRESH TOKEN
# ----------------------------
print_section("REFRESH ACCESS TOKEN")
cookies = {"refresh_token": refresh_cookie} if refresh_cookie else {}
r = requests.post(f"{BASE_URL}/auth/refresh", cookies=cookies)
print("Status:", r.status_code)
try:
    print("Response:", r.json())
except:
    print("Raw response:", r.text)

new_access_token = r.json().get("access_token") if r.status_code == 200 else None

# ----------------------------
# 5. LOGOUT (delete refresh cookie)
# ----------------------------
print_section("LOGOUT USER")
r = requests.post(f"{BASE_URL}/auth/logout")
print("Status:", r.status_code)
try:
    print("Response:", r.json())
except:
    print("Raw response:", r.text)
