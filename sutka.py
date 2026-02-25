import requests
import re
from datetime import datetime

URL = "https://www.sutka.eu/"

response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
html = response.text.replace("\n", " ")

# najdeme procenta
percent_match = re.search(r"(\d+)\s*%", html)

# najdeme Bazén
pool_match = re.search(r"(\d+)\s*\(Baz", html)

# najdeme Aquapark
aquapark_match = re.search(r"(\d+)\s*\(Aquapark", html)

if not (percent_match and pool_match and aquapark_match):
    print("Obsazenost nenalezena – HTML struktura jiná")
    exit(0)  # důležité – nezpůsobí chybu workflow

percent = percent_match.group(1)
pool = pool_match.group(1)
aquapark = aquapark_match.group(1)

timestamp = datetime.utcnow().isoformat()

line = f"{timestamp},{percent},{pool},{aquapark}\n"

with open("data.csv", "a", encoding="utf-8") as f:
    f.write(line)

print("Uloženo:", line)
