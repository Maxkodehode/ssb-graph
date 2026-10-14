import requests
import matplotlib.pyplot as plt
import json
import sys

BASE = "https://data.ssb.no/api/pxwebapi/v2"
QUERY = sys.argv[1] if len(sys.argv) > 1 else ""

if QUERY and not QUERY.startswith("/"):
    response = requests.get(f"{BASE}/tables", params={"lang": "en", "query": QUERY})

else:
    response = requests.get(f"{BASE}/tables{QUERY}", params={"lang": "en"})
    

if not response.ok:
    print(f"Error {response.status_code}: {response.text}")
    sys.exit(1)
    
data = response.json()
outfile = "table.json"

with open (outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Saved to {outfile}")