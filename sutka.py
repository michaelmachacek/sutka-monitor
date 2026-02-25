import matplotlib
matplotlib.use("Agg")

import requests
import re
from datetime import datetime
import matplotlib.pyplot as plt
import csv
import os

URL = "https://www.sutka.eu/"
DATA_FILE = "data.csv"
GRAPH_FILE = "graf.png"

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

# === 2) Načíst historická data ===

timestamps = []
percents = []
pools = []
aquaparks = []

if os.path.exists(DATA_FILE):

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) >= 4:
                try:
                    timestamps.append(datetime.fromisoformat(row[0]))
                    percents.append(int(row[1]))
                    pools.append(int(row[2]))
                    aquaparks.append(int(row[3]))
                except:
                    continue

# === 3) Vykreslit graf ===

if len(percents) > 0:

    plt.figure(figsize=(12,6))

    plt.plot(timestamps, percents, label="Obsazenost (%)")
    plt.plot(timestamps, pools, label="Bazén (počet)")
    plt.plot(timestamps, aquaparks, label="Aquapark (počet)")

    plt.xlabel("Čas")
    plt.ylabel("Hodnota")
    plt.title("Vývoj obsazenosti - Aquacentrum Šutka")
    plt.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(GRAPH_FILE)
    plt.close()

    print("Graf aktualizován")
