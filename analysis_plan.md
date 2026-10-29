# Analysis plan: Do security company shares move with geopolitical risk?

Written October 29, 2026, before any share-price data were downloaded or any result was computed.
Changes after this date are listed at the bottom with the reason.

## Question
When world tension rises, do the shares of listed private security companies do better or worse
than their home stock market? Investors might expect more demand for guarding and secure
logistics in tense times, or they might see these firms as ordinary service businesses that are
hurt like everyone else. A result of "no relationship" is reported in the same way as any other.

## Companies (guarding and cash-handling firms only)
| Company | Home market | Compared with |
|---|---|---|
| SECOM | Tokyo | TOPIX |
| Sohgo Security Services (ALSOK) | Tokyo | TOPIX |
| Securitas | Stockholm | OMX Stockholm 30 |
| Loomis | Stockholm (listed from December 2008) | OMX Stockholm 30 |
| Prosegur | Madrid | IBEX 35 |
| Brink's | New York | S&P 500 |
| G4S | London (shares cancelled 5 May 2021) | FTSE 100, only if its history is available |

Defence contractors (for example KBR or CACI) are left out on purpose: they sell services to
militaries, which is a different business and a different question.

## Data
- Geopolitical Risk Index (GPR), monthly, Caldara and Iacoviello, downloaded October 29, 2026
  from https://www.matteoiacoviello.com/gpr.htm (CC BY). Also its two parts: threats (GPRT) and
  acts (GPRA).
- Month-end share prices and index levels, adjusted for splits. Source and its terms are recorded
  in data/README.md.
- Period: January 2000 (or the first month a company is listed) to September 2026, the latest
  month of the index.

## Outcome
Abnormal return: the monthly log return of a company's share minus the monthly log return of its
home market index, both in local currency (so exchange rates drop out).

## Measure of risk
The monthly change in the log of the GPR index (how much tension rose or fell that month).

## Main tests
1. Portfolio test: each month, the equal-weighted average abnormal return of all companies
   listed that month, regressed on the change in log GPR. Newey-West standard errors, 3 lags.
2. Company by company: the same regression for each company separately.
3. Biggest shocks: the 10 months since 2000 with the largest rise in log GPR. The average
   portfolio abnormal return in those months, and a test of whether it differs from zero.

## Checks fixed in advance
- Threats (GPRT) and acts (GPRA) in place of the overall index.
- A market-model version: company return regressed on market return and the change in log GPR,
  instead of subtracting the market return one for one.
- Start in January 2005 instead of January 2000.
- Japanese companies only, and non-Japanese companies only.

## What the result cannot show
These are correlations over time, not causes: a month of high tension is often also a month of
other news. There are only six or seven companies, so company-level estimates are noisy, and
running several tests means one of them may look significant by chance. The project reports all
of them, not only the ones that look interesting.

## Changes after writing
All of these were made on October 29, 2026, after checking which price series were available
and before any return or result was computed.
- Price source: Stooq refused downloads from the computer used for this project, so prices come
  from Yahoo Finance (through the yfinance package) instead. Neither site allows its data to be
  republished, so the repository has the download script, not the price files.
- Prices: month-end closing prices adjusted for splits but not for dividends, for companies and
  indices alike, so both sides of the abnormal return are price returns.
- Japan: Yahoo Finance has no TOPIX history, so the Japanese companies are compared with the
  Nikkei 225 instead.
- Sweden: Yahoo Finance has OMX Stockholm 30 only from November 2008, so Securitas enters the
  sample in December 2008 (Loomis was listed in December 2008 anyway).
- G4S: Yahoo Finance has no history for it, so it is left out.
- Sohgo Security (ALSOK) has prices from October 2002.
- Two months are dropped because a spin-off cut the share price mechanically (shareholders
  received shares in the new company, so the fall is not a loss): Brink's in November 2008
  (Brink's Home Security distributed October 31, 2008) and Securitas in December 2008 (Loomis
  distributed, first trading day December 9, 2008). Found while screening the largest monthly
  moves, before any test was run.
