import requests
import matplotlib.pyplot as plt
import json

BASE = "https://data.ssb.no/api/pxwebapi/v2"

response = requests.get(f"{BASE}/tables", params={"lang": "en", "pageSize": 5})
resp = requests.get(f"{BASE}/navigation")
data = response.json()

with open ("tables.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {len(data['tables'])} tables to tables_test.json")