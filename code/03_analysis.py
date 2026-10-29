"""Tests fixed in analysis_plan.md. Reads data/clean/panel.csv; writes output/tables and figures/."""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "output" / "tables", ROOT / "figures"
TAB.mkdir(parents=True, exist_ok=True); FIG.mkdir(parents=True, exist_ok=True)
HAC = {"cov_type": "HAC", "cov_kwds": {"maxlags": 3}}

p = pd.read_csv(ROOT / "data" / "clean" / "panel.csv")


def portfolio(df):
    """Equal-weighted average across the companies listed each month."""
    cols = ["abnormal", "ret_firm", "ret_market", "dlog_GPR", "dlog_GPRT", "dlog_GPRA"]
    return df.groupby("month", as_index=False)[cols].mean().assign(n_firms=df.groupby("month").size().values)


def fit(df, formula, label, sample, risk="dlog_GPR"):
    m = smf.ols(formula, data=df).fit(**HAC)
    lo, hi = m.conf_int().loc[risk]
    return {"test": label, "sample": sample, "months": int(m.nobs), "coef": m.params[risk],
            "se": m.bse[risk], "p": m.pvalues[risk], "ci_low": lo, "ci_high": hi}


rows = []
port = portfolio(p)
# Main test 1: portfolio.
rows.append(fit(port, "abnormal ~ dlog_GPR", "1. portfolio abnormal return on change in log GPR", "all"))
# Checks fixed in advance.
rows.append(fit(port, "abnormal ~ dlog_GPRT", "check: threats (GPRT)", "all", "dlog_GPRT"))
rows.append(fit(port, "abnormal ~ dlog_GPRA", "check: acts (GPRA)", "all", "dlog_GPRA"))
rows.append(fit(port, "ret_firm ~ ret_market + dlog_GPR", "check: market model", "all"))
rows.append(fit(port[port.month >= "2005-01"], "abnormal ~ dlog_GPR", "check: from January 2005", "2005-01 on"))
for grp in ["Japan", "Other"]:
    rows.append(fit(portfolio(p[p.group == grp]), "abnormal ~ dlog_GPR", f"check: {grp} companies only", grp))
# Main test 2: company by company.
for firm, g in p.groupby("firm"):
    rows.append(fit(g, "abnormal ~ dlog_GPR", "2. company", firm))
res = pd.DataFrame(rows)
res.to_csv(TAB / "regressions.csv", index=False)

# Main test 3: the 10 months since 2000 with the largest rise in log GPR.
top = port.nlargest(10, "dlog_GPR").sort_values("month")
top.to_csv(TAB / "top10_gpr_months.csv", index=False)
m = smf.ols("abnormal ~ 1", data=top).fit()
shock = pd.DataFrame([{"months": len(top), "mean_abnormal": m.params["Intercept"], "se": m.bse["Intercept"],
                       "p": m.pvalues["Intercept"], "mean_all_months": port["abnormal"].mean()}])
shock.to_csv(TAB / "top10_test.csv", index=False)

# Summary: months and average returns per company.
summ = p.groupby("firm").agg(first=("month", "min"), last=("month", "max"), months=("month", "size"),
                             mean_abnormal=("abnormal", "mean"), sd_abnormal=("abnormal", "std"))
summ.to_csv(TAB / "summary_by_company.csv")

# Figure: portfolio abnormal return against the change in log GPR.
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.scatter(100 * port["dlog_GPR"], 100 * port["abnormal"], s=10, color="black", alpha=0.5)
b = res.iloc[0]
x = np.linspace(port["dlog_GPR"].min(), port["dlog_GPR"].max(), 50)
icpt = smf.ols("abnormal ~ dlog_GPR", data=port).fit().params["Intercept"]
ax.plot(100 * x, 100 * (icpt + b["coef"] * x), color="grey")
ax.axhline(0, color="grey", linewidth=0.5); ax.axvline(0, color="grey", linewidth=0.5)
ax.set_xlabel("Change in geopolitical risk that month (log points x 100)")
ax.set_ylabel("Security shares minus home market (%)")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(FIG / "abnormal_vs_gpr.png", dpi=200)

# Figure: cumulative abnormal return of the portfolio, with the GPR index.
gpr = pd.read_excel(ROOT / "data" / "raw" / "data_gpr_export.xls")[["month", "GPR"]].dropna()
gpr = gpr[(gpr.month >= "2000-01-01") & (gpr.month <= "2026-09-30")]
fig, ax1 = plt.subplots(figsize=(7.5, 4))
dates = pd.to_datetime(port["month"] + "-01")
ax1.plot(dates, 100 * port["abnormal"].cumsum(), color="black", linewidth=1.2, label="Security shares minus home market (cumulative)")
ax1.set_ylabel("Cumulative abnormal return (log points x 100)")
ax2 = ax1.twinx()
ax2.plot(pd.to_datetime(gpr["month"]), gpr["GPR"], color="grey", linewidth=0.8, label="Geopolitical Risk Index (right)")
ax2.set_ylabel("Geopolitical Risk Index")
h1, l1 = ax1.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left", fontsize=8)
ax1.spines[["top"]].set_visible(False); ax2.spines[["top"]].set_visible(False)
fig.tight_layout(); fig.savefig(FIG / "cumulative_and_gpr.png", dpi=200)

pd.set_option("display.width", 200)
print(res.round(4).to_string(index=False))
print(top[["month", "dlog_GPR", "abnormal", "n_firms"]].round(4).to_string(index=False))
print(shock.round(4).to_string(index=False))
print(summ.round(4))
