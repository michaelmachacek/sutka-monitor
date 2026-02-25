import matplotlib
matplotlib.use("Agg")

import requests
import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import csv
import os

URL = "https://www.sutka.eu/"
DATA_FILE = "data.csv"

# === 1) Stáhnout aktuální data ===

response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
html = response.text.replace("\n", " ")

pattern = re.search(
    r"Aktuální počet návštěvníků:.*?<strong>(\d+)%</strong>.*?<strong>(\d+)</strong>\s*\(Bazén\).*?<strong>(\d+)</strong>\s*\(Aquapark\)",
    html,
    re.IGNORECASE
)

if pattern:
    percent = pattern.group(1)
    pool = pattern.group(2)
    aquapark = pattern.group(3)

    timestamp = datetime.utcnow().isoformat()
    line = f"{timestamp},{percent},{pool},{aquapark}\n"

    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(line)

    print("Uloženo:", line)
else:
    print("Obsazenost nenalezena")

# === 2) Načíst historická data (posledních 24h) ===

timestamps = []
percents = []
pools = []
aquaparks = []

now = datetime.utcnow()
limit = now - timedelta(hours=24)

if os.path.exists(DATA_FILE):

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) >= 4:
                try:
                    t = datetime.fromisoformat(row[0])
                    if t >= limit:
                        timestamps.append(t)
                        percents.append(int(row[1]))
                        pools.append(int(row[2]))
                        aquaparks.append(int(row[3]))
                except:
                    continue

# === 3) Vykreslit graf ===

if len(percents) > 0:

    today_str = now.strftime("%Y-%m-%d")
    graph_file = f"graf_{today_str}.png"

    fig, ax1 = plt.subplots(figsize=(12,6))

    # levá osa = počty lidí
    ax1.plot(timestamps, pools, label="Bazén (počet)")
    ax1.plot(timestamps, aquaparks, label="Aquapark (počet)")
    ax1.set_xlabel("Čas (UTC)")
    ax1.set_ylabel("Počet lidí")

    # pravá osa = procenta
    ax2 = ax1.twinx()
    ax2.plot(timestamps, percents, linestyle="--", label="Obsazenost (%)")
    ax2.set_ylabel("Obsazenost (%)")

    # legenda (sloučí obě osy)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.title("Obsazenost Šutka – posledních 24h")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(graph_file)
    plt.close()

    print("Graf aktualizován:", graph_file)
