# FOMC Statement Scraper (2000–Present)

This project builds a clean local corpus of **FOMC meeting statements** by scraping them directly from the Federal Reserve website, starting in **year 2000** through the present.

It automatically:

- Discovers all eligible FOMC *meeting* statements (not conference calls, not notation votes)
- Handles both modern and legacy webpage layouts
- Extracts and cleans the main statement text
- Removes boilerplate (e.g. “For immediate release”) and voting sections
- Saves each statement as a plain-text file named by date (`YYYYMMDD.txt`)

The result is a reproducible, machine-readable archive of FOMC policy statements suitable for NLP, economic analysis, or historical research.

---
