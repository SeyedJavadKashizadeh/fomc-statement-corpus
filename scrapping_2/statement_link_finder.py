import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from configuration_1 import config

out = []
seen = set()

def add(u):
    if u not in seen:
        out.append(u)
        seen.add(u)

# -------- historic years (>=2000), meeting statements only --------
index_html = requests.get(config.INDEX).content.decode("utf-8-sig")
index_soup = BeautifulSoup(index_html, "html.parser")

years = []
for a in index_soup.find_all("a", href=True):
    h = urljoin(config.BASE, a["href"])
    if "fomchistorical" in h and h[-8:-4].isdigit() and int(h[-8:-4]) >= 2000:
        years.append(h)

years = list(dict.fromkeys(years))

for y in years:
    y_soup = BeautifulSoup(requests.get(y).content.decode("utf-8-sig"), "html.parser")
    for a in y_soup.find_all("a", href=True):
        if a.get_text(strip=True) != "Statement":
            continue

        h5 = a.find_previous("h5")
        if not h5:
            continue

        title = h5.get_text(" ", strip=True).lower()
        if "meeting" not in title or "conference call" in title:
            continue

        add(urljoin(config.BASE, a["href"]))

# -------- calendar pages (>=2021) --------
cal_html = requests.get(config.CAL).content.decode("utf-8-sig")
cal_soup = BeautifulSoup(cal_html, "html.parser")

pages = {config.CAL}
for a in cal_soup.find_all("a", href=True):
    u = urljoin(config.CAL, a["href"]).split("#", 1)[0].split("?", 1)[0]
    m = config.cal_year_re.search(u)
    if m and int(m.group(1)) >= 2021:
        pages.add(u)

for p in pages:
    p_soup = BeautifulSoup(requests.get(p).content.decode("utf-8-sig"), "html.parser")

    for meeting in p_soup.select("div.fomc-meeting"):
        date_div = meeting.select_one("div.fomc-meeting__date")
        date_txt = date_div.get_text(" ", strip=True).lower() if date_div else ""

        # Skip notation votes
        if "notation vote" in date_txt:
            print("Skipping notation vote")
            continue

        # Only collect links within this meeting block
        for a in meeting.find_all("a", href=True):
            u = urljoin(p, a["href"]).split("#", 1)[0].split("?", 1)[0]
            if config.stmt_re.search(u):
                add(u)

out.sort(key=lambda u: re.compile(r"(\d{8})").search(u).group(1), reverse=True)

with open(os.path.join(config.statement_root, "statement_links.txt"), "w", encoding="utf-8") as f:
    for u in out:
        f.write(u + "\n")


