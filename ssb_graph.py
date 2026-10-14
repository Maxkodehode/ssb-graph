import sys
import requests
import json
import matplotlib.pyplot as plt

BASE = "https://data.ssb.no/api/pxwebapi/v2"
TABLE = sys.argv[1] if len(sys.argv) > 1 else "10280"

if len(sys.argv) > 2:
    with open(sys.argv[2]) as f:
        body = json.load(f)
else:
    body = {
  "selection": [
    {"variableCode": "Hovedpost2", "valueCodes": ["00"]},
    {"variableCode": "ContentsCode", "valueCodes": ["Brutto"]},
    {"variableCode": "Tid", "valueCodes": ["*"]}
  ]
}

response = requests.post(f"{BASE}/tables/{TABLE}/data", json=body)
data = response.json()

with open(f"data_{TABLE}.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved data_{TABLE}.json")