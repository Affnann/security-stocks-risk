"""Download the data.

1. Geopolitical Risk Index, monthly (Caldara and Iacoviello), saved to data/raw/data_gpr_export.xls.
2. Month-end share prices and index levels from Yahoo Finance, saved to data/raw/prices/.
   Yahoo Finance does not allow its data to be republished, so data/raw/prices/ is not in the
   repository; run this script to create it.
"""
from pathlib import Path
import time
import requests
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PRICES = RAW / "prices"
PRICES.mkdir(parents=True, exist_ok=True)

GPR_URL = "https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls"

# Yahoo Finance symbol -> file name
SYMBOLS = {
    "9735.T": "secom",
    "2331.T": "sohgo_alsok",
    "SECU-B.ST": "securitas",
    "LOOMIS.ST": "loomis",
    "PSG.MC": "prosegur",
    "BCO": "brinks",
    "^N225": "index_nikkei225",
    "^OMX": "index_omxs30",
    "^IBEX": "index_ibex35",
    "^GSPC": "index_sp500",
}
START, END = "1999-12-01", "2026-10-01"  # END is exclusive: last month is September 2026

r = requests.get(GPR_URL, timeout=60)
r.raise_for_status()
(RAW / "data_gpr_export.xls").write_bytes(r.content)
print("GPR:", len(r.content), "bytes")

for symbol, name in SYMBOLS.items():
    d = yf.download(symbol, start=START, end=END, interval="1mo", auto_adjust=False, progress=False)
    if d.empty:
        raise SystemExit(f"No data for {symbol}")
    d.columns = d.columns.get_level_values(0)
    d.index.name = "month"
    d.to_csv(PRICES / f"{name}.csv")
    print(f"{symbol:10s} {len(d):4d} months, {d.index[0]:%Y-%m} to {d.index[-1]:%Y-%m}")
    time.sleep(2)
