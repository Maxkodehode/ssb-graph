import json, sys
import matplotlib.pyplot as plt

def plot_json_stat(filepath):
    with open(filepath) as f:
        data = json.load(f)

    time_idx = data["id"].index("Tid")
    times = list(data["dimension"]["Tid"]["category"]["label"].values())

    values = data["value"]

    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker="o")
    plt.title(data["label"])
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graph.png")
    print("Saved graph.png")

if __name__ == "__main__":
    plot_json_stat(sys.argv[1])