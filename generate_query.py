import sys
import requests
import json

BASE = "https://data.ssb.no/api/pxwebapi/v2"

if len(sys.argv) < 2:
    print("Usage: python generate_query.py <table_id>")
    sys.exit(1)

TABLE = sys.argv[1]

response = requests.get(f"{BASE}/tables/{TABLE}/metadata", params={"lang": "en"})
if not response.ok:
    print(f"Error {response.status_code}: {response.text}")
    sys.exit(1)

metadata = response.json()

time_dim = metadata.get("role", {}).get("time", ["Tid"])[0]

query_config = {
    "table": TABLE,
    "label": metadata.get("label", ""),
    "updated": metadata.get("updated", ""),
    "selection": []
}

for var_name, var_info in metadata["dimension"].items():
    category = var_info["category"]
    var_label = var_info.get("label", var_name)

    all_values = {}
    for code in category.get("index", {}):
        label = category.get("label", {}).get(code, code)
        all_values[code] = label

    if var_name == time_dim:
        selected = ["*"]
    elif var_info.get("extension", {}).get("elimination"):
        default = var_info["extension"].get("eliminationValueCode", list(all_values.keys())[0])
        selected = [default]
    else:
        selected = [list(all_values.keys())[0]]

    query_config["selection"].append({
        "variableCode": var_name,
        "label": var_label,
        "allValues": all_values,
        "selected": selected
    })

outfile = f"meta_json/query_{TABLE}.json"
with open(outfile, "w", encoding="utf-8") as f:
    json.dump(query_config, f, indent=2, ensure_ascii=False)

print(f"Saved {outfile}")
print(f"Table: {query_config['label']}")
for s in query_config["selection"]:
    total = len(s["allValues"])
    sel_labels = [s["allValues"].get(c, c) for c in s["selected"]]
    display = "*" if s["selected"] == ["*"] else ", ".join(sel_labels)
    print(f"  {s['variableCode']} ({s['label']}): {display}  [{total} available]")