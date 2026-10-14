import json
import sys
import plotly.graph_objects as go

def plot_json_stat(filepath):
    with open(filepath) as f:
        data = json.load(f)

    id_order = data["id"]
    sizes = data["size"]
    values = data["value"]

    rows = []
    for i, val in enumerate(values):
        remainder = i
        row = {"value": val}
        for dim_idx, dim_name in enumerate(id_order):
            dim_size = sizes[dim_idx]
            code_index = remainder % dim_size
            remainder //= dim_size
            dim = data["dimension"][dim_name]
            code = list(dim["category"]["index"].keys())[code_index]
            label = dim["category"]["label"].get(code, code)
            row[dim_name] = label
        rows.append(row)
    time_dim = data["role"]["time"][0]
    varying = [d for d in id_order if d != time_dim and sizes[id_order.index(d)] > 1]

    fig = go.Figure()

    if varying:
        color_dim = varying[0]
        groups = {}
        for row in rows:
            key = row[color_dim]
            if key not in groups:
                groups[key] = {"x": [], "y": []}
            groups[key]["x"].append(row[time_dim])
            groups[key]["y"].append(row["value"])

        for key, group in groups.items():
            fig.add_trace(go.Scatter(
                x=group["x"], y=group["y"],
                mode="lines+markers",
                name=key
            ))
    else:
        x = [row[time_dim] for row in rows]
        y = [row["value"] for row in rows]
        fig.add_trace(go.Scatter(
            x=x, y=y, mode="lines+markers", name=""
        ))

    fig.update_layout(
        title=data.get("label", ""),
        xaxis_title=time_dim,
        yaxis_title="Value",
        template="plotly_white"
    )

    fig.write_html("graph.html")
    print(f"Saved graph.html — {len(rows)} data points")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python plot_data.py <data_file.json>")
        sys.exit(1)
    plot_json_stat(sys.argv[1])