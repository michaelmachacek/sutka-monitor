import requests
import re
from datetime import datetime

URL = "https://www.sutka.eu/"

response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
html = response.text.replace("\n", " ")

# hledáme konkrétní blok s návštěvností
pattern = re.search(
    r"Aktuální počet návštěvníků:.*?<strong>(\d+)%</strong>.*?<strong>(\d+)</strong>\s*\(Bazén\).*?<strong>(\d+)</strong>\s*\(Aquapark\)",
    html,
    re.IGNORECASE
)

if not pattern:
    print("Obsazenost nenalezena")
    exit(0)

percent = pattern.group(1)
pool = pattern.group(2)
aquapark = pattern.group(3)

timestamp = datetime.utcnow().isoformat()
line = f"{timestamp},{percent},{pool},{aquapark}\n"

with open("data.csv", "a", encoding="utf-8") as f:
    f.write(line)

print("Uloženo:", line)
