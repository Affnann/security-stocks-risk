# Data

## Geopolitical Risk Index

- **File:** `raw/data_gpr_export.xls` (monthly), included in this repository.
- **Source:** Dario Caldara and Matteo Iacoviello, https://www.matteoiacoviello.com/gpr.htm
- **Downloaded:** October 29, 2026 (the site's monthly file was last updated October 1, 2026; the latest months are preliminary).
- **Licence:** Creative Commons BY, as stated on the source page. Data downloaded from https://www.matteoiacoviello.com/gpr.htm on October 29, 2026.
- **Paper:** Caldara, Dario and Matteo Iacoviello (2022). "Measuring Geopolitical Risk." *American Economic Review* 112(4): 1194–1225.
- **Variables used:** `GPR` (overall index), `GPRT` (threats), `GPRA` (acts), monthly from January 2000 to September 2026.

## Share prices and market indices

- **Source:** Yahoo Finance, through the `yfinance` package, monthly bars.
- **Downloaded:** October 29, 2026.
- **Not included in this repository:** Yahoo Finance does not allow its data to be republished. `code/01_download.py` saves the files to `raw/prices/`.
- **Price used:** the month-end close, adjusted for splits but not for dividends (`Close` with `auto_adjust=False`), for companies and indices alike.

| Yahoo Finance symbol | Series | File | First month |
|---|---|---|---|
| 9735.T | SECOM | `secom.csv` | January 2000 |
| 2331.T | Sohgo Security Services (ALSOK) | `sohgo_alsok.csv` | October 2002 |
| SECU-B.ST | Securitas, B shares | `securitas.csv` | January 2000 |
| LOOMIS.ST | Loomis | `loomis.csv` | December 2008 |
| PSG.MC | Prosegur | `prosegur.csv` | January 2000 |
| BCO | Brink's | `brinks.csv` | December 1999 |
| ^N225 | Nikkei 225 | `index_nikkei225.csv` | December 1999 |
| ^OMX | OMX Stockholm 30 | `index_omxs30.csv` | November 2008 |
| ^IBEX | IBEX 35 | `index_ibex35.csv` | December 1999 |
| ^GSPC | S&P 500 | `index_sp500.csv` | December 1999 |

Spot check: the December 2023 closes match published values (Nikkei 225: 33,464.17; S&P 500: 4,769.83).

## Clean panel

`clean/panel.csv` is built by `code/02_build_panel.py` and is not included, because it is derived from Yahoo Finance prices. One row per company per month:

| Column | Meaning |
|---|---|
| `month` | Year and month |
| `ret_firm` | Monthly log return of the company's share |
| `ret_market` | Monthly log return of its home market index |
| `abnormal` | `ret_firm` minus `ret_market` |
| `firm`, `group` | Company name; `Japan` or `Other` |
| `dlog_GPR`, `dlog_GPRT`, `dlog_GPRA` | Monthly change in the log of each risk index |

Two months are removed because a spin-off lowered the share price mechanically: Brink's in November 2008 (Brink's Home Security was distributed to shareholders on October 31, 2008) and Securitas in December 2008 (Loomis was distributed to shareholders; first trading day December 9, 2008).

G4S is not included: its shares stopped trading on May 5, 2021, and Yahoo Finance has no history for it.
