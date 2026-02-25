import requests
from datetime import datetime

URL = "https://www.sutka.eu/"

response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
html = response.text

# uložíme HTML pro kontrolu
with open("debug.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML uloženo do debug.html")
