import requests
import json

# user data input
settings_data = {
    "users": ["Alice", "Bob"],
    "topics": ["Math", "Science"]
}

# send setting request
res = requests.post("http://127.0.0.1:5000/api/settings", json=settings_data)
print("Settings Response:", res.status_code, res.json())

# roll dice request
roll_data = {
    "player": "Alice"
}

res = requests.post("http://127.0.0.1:5000/api/roll-dice", json=roll_data)
print("Roll Dice Response:", res.status_code, res.json())
