import requests
import re
from datetime import datetime

URL = "https://www.sutka.eu/"

response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
html = response.text

pattern = re.search(
    r"(\d+)%\s*obsazenost:\s*\|\s*(\d+)\s*\(Baz[eé]n\)\s*\|\s*(\d+)\s*\(Aquapark\)",
    html.replace("\n", " "),
    re.IGNORECASE
)

if not pattern:
    raise Exception("Obsazenost nenalezena")

percent = pattern.group(1)
pool = pattern.group(2)
aquapark = pattern.group(3)

timestamp = datetime.utcnow().isoformat()

line = f"{timestamp},{percent},{pool},{aquapark}\n"

with open("data.csv", "a", encoding="utf-8") as f:
    f.write(line)

print("Uloženo:", line)
