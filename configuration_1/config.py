import re

BASE = "https://www.federalreserve.gov"
INDEX = BASE + "/monetarypolicy/fomc_historical_year.htm"
CAL   = BASE + "/monetarypolicy/fomccalendars.htm"

stmt_re = re.compile(r"/newsevents/pressreleases/monetary\d{8}a\.htm$", re.I)
cal_year_re = re.compile(r"/monetarypolicy/fomccalendars(\d{4})\.htm$", re.I)

statement_root = "YOUR_STATEMENT_DIRECTORY"
statement_text = f"{statement_root}/statement_text"
statement_diff = f"{statement_root}/statement_diff"


cut_after = [
        "voting for the monetary policy action",
        "voting for the fomc monetary policy action",
        "voting against the action",
        "In taking the discount rate action",
        "2000 Monetary Policy",
        "2001 Monetary Policy",
        "2002 Monetary Policy",
    ]

cut_before = ["For immediate release",
              ]