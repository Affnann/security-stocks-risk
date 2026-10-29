"""Build the monthly panel of abnormal returns and changes in geopolitical risk.

Abnormal return = monthly log return of the company's share minus that of its home market index,
both from month-end closes adjusted for splits (not dividends). See analysis_plan.md.
Writes data/clean/panel.csv (not in the repository, because it is built from Yahoo Finance prices).
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, CLEAN = ROOT / "data" / "raw", ROOT / "data" / "clean"
CLEAN.mkdir(parents=True, exist_ok=True)

COMPANIES = {  # company file -> (display name, home index file, country group)
    "secom": ("SECOM", "index_nikkei225", "Japan"),
    "sohgo_alsok": ("Sohgo Security (ALSOK)", "index_nikkei225", "Japan"),
    "securitas": ("Securitas", "index_omxs30", "Other"),
    "loomis": ("Loomis", "index_omxs30", "Other"),
    "prosegur": ("Prosegur", "index_ibex35", "Other"),
    "brinks": ("Brink's", "index_sp500", "Other"),
}


def log_returns(name):
    p = pd.read_csv(RAW / "prices" / f"{name}.csv", parse_dates=["month"]).set_index("month")["Close"]
    p.index = p.index.to_period("M")
    return np.log(p).diff()


gpr = pd.read_excel(RAW / "data_gpr_export.xls")[["month", "GPR", "GPRT", "GPRA"]].dropna()
gpr["month"] = pd.to_datetime(gpr["month"]).dt.to_period("M")
gpr = gpr.set_index("month")
dg = np.log(gpr).diff().add_prefix("dlog_")

rows = []
for firm, (label, index, group) in COMPANIES.items():
    r_firm, r_mkt = log_returns(firm), log_returns(index)
    d = pd.DataFrame({"ret_firm": r_firm, "ret_market": r_mkt}).dropna()
    d["abnormal"] = d["ret_firm"] - d["ret_market"]
    d["firm"], d["group"] = label, group
    rows.append(d)

panel = pd.concat(rows).join(dg, how="inner").reset_index()
panel = panel[(panel["month"] >= pd.Period("2000-01", "M")) & (panel["month"] <= pd.Period("2026-09", "M"))]
panel["month"] = panel["month"].astype(str)
# Spin-off months: the share price fell because shareholders received shares in a new company.
SPINOFFS = [("Brink's", "2008-11"), ("Securitas", "2008-12")]
for firm, month in SPINOFFS:
    panel = panel[~((panel["firm"] == firm) & (panel["month"] == month))]
panel.to_csv(CLEAN / "panel.csv", index=False)
print(panel.groupby("firm")["month"].agg(["count", "min", "max"]))
