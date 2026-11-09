import hashlib
import hmac
import os

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()
API_KEY = os.getenv("API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# Retry உள்ள session
session = requests.Session()
retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retry))

# முதல் 5 users
users = session.get("https://jsonplaceholder.typicode.com/users", timeout=10).json()
for u in users[:5]:
    print(f"{u['id']} - {u['name']} - {u['email']}")

# Nested JSON, .get() மட்டும்
first = users[0]
address = first.get("address", {})
city = address.get("city", "Not Available")
lat = address.get("geo", {}).get("lat", "Not Available")
zipcode = address.get("zipcode", "Not Available")
company = first.get("company", {}).get("name", "Not Available")
print(f"City: {city} | Latitude: {lat} | Zip: {zipcode} | Company: {company}")


# HMAC verify
def verify_signature(payload: str, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


payload = '{"event": "employee_created"}'
signature = hmac.new(
    WEBHOOK_SECRET.encode(), payload.encode(), hashlib.sha256
).hexdigest()

valid = verify_signature(payload, signature, WEBHOOK_SECRET)
tampered = verify_signature('{"event": "hacked"}', signature, WEBHOOK_SECRET)
wrong = verify_signature(payload, signature, "wrong_secret")
print(f"Valid: {valid} | Tampered: {tampered} | Wrong secret: {wrong}")
