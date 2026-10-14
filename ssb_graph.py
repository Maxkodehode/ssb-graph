import sys
import requests
import json

BASE = "https://data.ssb.no/api/pxwebapi/v2"

if len(sys.argv) < 2:
    print("Usage: python ssb_graph.py <table_id> [query_file]")
    sys.exit(1)

TABLE = sys.argv[1]

query_path = sys.argv[2] if len(sys.argv) > 2 else f"meta_json/query_{TABLE}.json"

with open(query_path) as f:
    body = json.load(f)

response = requests.post(f"{BASE}/tables/{TABLE}/data", json=body)
data = response.json()

with open(f"data_json/data_{TABLE}.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved data_json/data_{TABLE}.json")