import matplotlib
matplotlib.use("Agg")

import requests
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt
import csv
import os

URL = "https://www.sutka.eu/"
DATA_FILE = "data.csv"

CZ = ZoneInfo("Europe/Prague")

# --- 1) stáhnout aktuální hodnoty ---
response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
html = response.text.replace("\n", " ")

pattern = re.search(
    r"Aktuální počet návštěvníků:.*?<strong>(\d+)%</strong>.*?<strong>(\d+)</strong>\s*\(Bazén\).*?<strong>(\d+)</strong>\s*\(Aquapark\)",
    html,
    re.IGNORECASE
)

if pattern:
    percent = int(pattern.group(1))
    pool = int(pattern.group(2))
    aquapark = int(pattern.group(3))

    ts = datetime.now(CZ)  # český čas (včetně DST)

    # zapiš CSV robustně (žádné problémy s \n)
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        # volitelná hlavička, jen když soubor neexistuje
        if not file_exists:
            w.writerow(["timestamp", "percent", "pool", "aquapark"])
        w.writerow([ts.isoformat(timespec="seconds"), percent, pool, aquapark])

    print(f"Uloženo: {ts.isoformat(timespec='seconds')} {percent}% {pool} {aquapark}")
else:
    print("Obsazenost nenalezena (nezapisují se data).")

# --- 2) načti data za posledních 24h a udělej graf ---
now = datetime.now(CZ)
limit = now - timedelta(hours=24)

timestamps = []
percents = []
pools = []
aquaparks = []

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            # přeskoč hlavičku / špatné řádky
            if len(row) < 4 or row[0] == "timestamp":
                continue
            try:
                t = datetime.fromisoformat(row[0])
                if t >= limit:
                    timestamps.append(t)
                    percents.append(int(row[1]))
                    pools.append(int(row[2]))
                    aquaparks.append(int(row[3]))
            except:
                continue

if timestamps:
    today_str = now.strftime("%Y-%m-%d")
    graph_file = f"graf_{today_str}.png"

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # levá osa: počty lidí
    ax1.plot(timestamps, pools, label="Bazén (počet)")
    ax1.plot(timestamps, aquaparks, label="Aquapark (počet)")
    ax1.set_xlabel("Čas (ČR)")
    ax1.set_ylabel("Počet lidí")

    # pravá osa: procenta
    ax2 = ax1.twinx()
    ax2.plot(timestamps, percents, linestyle="--", label="Obsazenost (%)")
    ax2.set_ylabel("Obsazenost (%)")

    # legenda sloučená z obou os
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    last_time = timestamps[-1].strftime("%d.%m.%Y %H:%M")
    plt.title(f"Obsazenost Šutka – posledních 24h\nPoslední aktualizace: {last_time}")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.close()

    print("Graf uložen:", graph_file)
else:
    print("V posledních 24h nejsou žádná data pro graf.")
