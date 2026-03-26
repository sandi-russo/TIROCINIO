import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os

# --- Carica i dati ---
neo4j = pd.read_csv("results/benchmark_neo4j.csv")
oracle = pd.read_csv("results/benchmark_oracle_final.csv")
df = pd.concat([neo4j, oracle])

# Estrai scala dal nome del test
df["scale"] = df["test"].str.extract(r"_(\d+)$").astype(int)
df["algo"]  = df["test"].str.extract(r"^([A-Za-z]+)")

SCALES = [25, 50, 75, 100]
os.makedirs("results/grafici", exist_ok=True)

N = 35  # warm run
Z = 1.96

def get_vals(algo, db, col):
    rows = df[(df["algo"] == algo) & (df["db"] == db)]
    rows = rows.set_index("scale").reindex(SCALES)
    return rows[col].values

def ci(algo, db):
    rows = df[(df["algo"] == algo) & (df["db"] == db)]
    rows = rows.set_index("scale").reindex(SCALES)
    return (Z * rows["warm_std_ms"] / np.sqrt(N)).values

def plot_cold(algo, title, filename):
    neo_vals   = get_vals(algo, "Neo4j",  "cold_ms")
    ora_vals   = get_vals(algo, "Oracle", "cold_ms")

    x = np.arange(len(SCALES))
    w = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))
    bars1 = ax.bar(x - w/2, neo_vals, w, label="Neo4j",  color="#66bb6a", edgecolor="black", linewidth=0.6)
    bars2 = ax.bar(x + w/2, ora_vals, w, label="Oracle", color="#bdbdbd", edgecolor="black", linewidth=0.6)

    ax.bar_label(bars1, fmt="%.1f", padding=3, fontsize=9)
    ax.bar_label(bars2, fmt="%.1f", padding=3, fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{s}" for s in SCALES])
    ax.set_xlabel("Dimensione Dataset (%)")
    ax.set_ylabel("Tempo Prima Esecuzione (ms)")
    ax.set_title(f"{title} — Prima Esecuzione")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda v, _: f"{v:,.0f}"))

    plt.tight_layout()
    plt.savefig(f"results/grafici/{filename}_cold.png", dpi=150)
    plt.close()
    print(f"Salvato: {filename}_cold.png")

def plot_warm(algo, title, filename):
    neo_avg = get_vals(algo, "Neo4j",  "warm_avg_ms")
    ora_avg = get_vals(algo, "Oracle", "warm_avg_ms")
    neo_ci  = ci(algo, "Neo4j")
    ora_ci  = ci(algo, "Oracle")

    x = np.arange(len(SCALES))
    w = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))
    bars1 = ax.bar(x - w/2, neo_avg, w, label="Neo4j",
                   color="#66bb6a", edgecolor="black", linewidth=0.6,
                   yerr=neo_ci, capsize=5, error_kw={"elinewidth": 1.5, "ecolor": "black"})
    bars2 = ax.bar(x + w/2, ora_avg, w, label="Oracle",
                   color="#bdbdbd", edgecolor="black", linewidth=0.6,
                   yerr=ora_ci, capsize=5, error_kw={"elinewidth": 1.5, "ecolor": "black"})

    ax.bar_label(bars1, fmt="%.1f", padding=3, fontsize=9)
    ax.bar_label(bars2, fmt="%.1f", padding=3, fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{s}" for s in SCALES])
    ax.set_xlabel("Dimensione Dataset (%)")
    ax.set_ylabel("Tempo Medio Esecuzione (ms)")
    ax.set_title(f"{title} — Media Warm Run (CI 95%)")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda v, _: f"{v:,.0f}"))

    plt.tight_layout()
    plt.savefig(f"results/grafici/{filename}_warm.png", dpi=150)
    plt.close()
    print(f"Salvato: {filename}_warm.png")

# --- Genera tutti e 6 i grafici ---
plot_cold("ShortestPath", "Shortest Path", "shortest_path")
plot_warm("ShortestPath", "Shortest Path", "shortest_path")
plot_cold("PageRank",     "PageRank",      "pagerank")
plot_warm("PageRank",     "PageRank",      "pagerank")
plot_cold("WCC",          "WCC",           "wcc")
plot_warm("WCC",          "WCC",           "wcc")

print("\nTutti i grafici salvati in results/grafici/")