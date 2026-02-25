import requests
import re
from datetime import datetime

URL = "https://www.sutka.eu/"

response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
html = response.text.replace("\n", " ")

# uložit debug HTML
with open("debug.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Debug uložen")

# zkusíme najít jen procento
percent_match = re.search(r"(\d+)\s*%", html)

if not percent_match:
    print("Procento nenalezeno")
    exit(0)

percent = percent_match.group(1)

timestamp = datetime.utcnow().isoformat()
line = f"{timestamp},{percent}\n"

with open("data.csv", "a", encoding="utf-8") as f:
    f.write(line)

print("Uloženo:", line)
