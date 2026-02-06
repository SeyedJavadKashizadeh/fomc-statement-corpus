import os
import re
import requests
from bs4 import BeautifulSoup
from configuration_1 import config

def extract_statement_text_any(url: str) -> str:
    html = requests.get(url, timeout=30).content.decode("utf-8-sig")
    soup = BeautifulSoup(html, "html.parser")

    # --- Modern pressreleases pages ---
    article = soup.select_one("#article")
    if article:
        divs = article.select("div.col-xs-12.col-sm-8.col-md-8")
        body = max(divs, key=lambda d: len(d.find_all("p")), default=None)
        paras = [p.get_text(" ", strip=True) for p in (body.find_all("p") if body else article.find_all("p"))]
        text = "\n\n".join([p for p in paras if p])

    # --- Old table-based pages (like 2005) ---
    else:
        td = soup.select_one("table td") or soup.select_one("td") or soup.body
        if not td:
            print("NO MAIN CONTAINER:", url)
            return ""
        paras = [p.get_text(" ", strip=True) for p in td.find_all("p")] if td else []
        # fall back to whole text if <p> missing
        text = "\n\n".join([p for p in paras if p]) if paras else soup.get_text("\n", strip=True)

    # --- Cleanup rules (work for both eras) ---
    low = text.lower()

    # Cut everything from cut_after onward
    for marker in config.cut_after:
        m = marker.strip().lower()
        idx = low.find(m)
        if idx != -1:
            text = text[:idx].strip()
            low = text.lower()
            break

    # Cut everything before cut_before
    for marker in config.cut_before:
        m = marker.strip().lower()
        idx = low.find(m)
        if idx != -1:
            text = text[idx + len(m):].strip()
            low = text.lower()
            break

    # Normalize whitespace
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


with open(os.path.join(config.statement_root, "statement_links.txt"), "r", encoding="utf-8") as f:
    links = f.read().splitlines()


date_re = re.compile(r"(\d{8})")
os.makedirs(config.statement_root, exist_ok=True)

for u in links:
    rec = extract_statement_text_any(u)
    if not rec:
        continue

    ymd = date_re.search(u).group(1)
    path = os.path.join(config.statement_text, f"{ymd}.txt")

    with open(path, "w", encoding="utf-8") as f:
        f.write(rec)
