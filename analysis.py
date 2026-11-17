"""Reproduce every figure cited in the case-study README from the synthetic data.

Run:  python analysis.py
"""
import pandas as pd

df = pd.read_csv("synthetic_ad_data.csv", parse_dates=["date"])
df["week_start"] = df["date"] - pd.to_timedelta(df["date"].dt.weekday, unit="D")


def roas(rev, spend):
    return rev / spend if spend else float("nan")


tot_spend = df["ad_spend"].sum()
tot_rev = df["reported_revenue"].sum()
print("== Overall ==")
print(f"Spend ${tot_spend:,.2f} | Revenue ${tot_rev:,.2f} | Blended ROAS {roas(tot_rev, tot_spend):.2f}x")
print(f"Date range {df['date'].min().date()} to {df['date'].max().date()} | rows {len(df)}")

print("\n== Weekly (Monday start) ==")
wk = df.groupby("week_start").agg(
    spend=("ad_spend", "sum"),
    revenue=("reported_revenue", "sum"),
    days_with_data=("date", "nunique"),
)
wk["roas"] = wk["revenue"] / wk["spend"]
print(wk.round(2).to_string())

print("\n== Account level (combined-ID record kept separate) ==")
ac = df.groupby("account_id").agg(spend=("ad_spend", "sum"), revenue=("reported_revenue", "sum"),
                                  days=("date", "nunique"))
ac["share_pct"] = ac["spend"] / tot_spend * 100
ac["roas"] = ac["revenue"] / ac["spend"]
print(ac.round(2).sort_values("spend", ascending=False).to_string())

print("\n== Daily ==")
dy = df.groupby("date").agg(spend=("ad_spend", "sum"), revenue=("reported_revenue", "sum"))
dy["roas"] = dy["revenue"] / dy["spend"].where(dy["spend"] > 0)
print(dy.sort_values("roas").head(3).round(2).to_string())

zero = dy[dy["spend"] == 0]
print(f"\nZero-spend dates: {len(zero)} -> {[d.strftime('%b %d') for d in zero.index]}")
print(f"Revenue recorded on zero-spend dates: ${zero['revenue'].sum():,.2f} "
      f"({zero['revenue'].sum() / tot_rev * 100:.1f}% of total revenue)")

print("\n== ROAS sensitivity to questionable revenue ==")
rev_ex_zero = tot_rev - zero["revenue"].sum()
print(f"Blended ROAS, all revenue:                    {roas(tot_rev, tot_spend):.2f}x")
print(f"Blended ROAS, excl. zero-spend-date revenue:  {roas(rev_ex_zero, tot_spend):.2f}x")
first = wk.iloc[0]
rev_ex_first = tot_rev - first["revenue"]
spend_ex_first = tot_spend - first["spend"]
print(f"Blended ROAS, excl. first (outlier) week:     {roas(rev_ex_first, spend_ex_first):.2f}x")
print(f"Blended ROAS, excl. both:                     "
      f"{roas(rev_ex_first - zero[zero.index >= wk.index[1]]['revenue'].sum(), spend_ex_first):.2f}x")

print("\n== Combined-ID record ==")
print(df[df["account_id"].str.contains(",")].to_string(index=False))

print("\n== Budget pacing vs assumed $500/day (spending dates only) ==")
active = dy[dy["spend"] > 0]
print(f"Days with spend {len(active)} | avg daily spend ${active['spend'].mean():,.2f} | "
      f"days above $500: {(active['spend'] > 500).sum()} | days below: {(active['spend'] < 500).sum()}")
print(f"Cumulative spend ${tot_spend:,.2f} vs ${500 * len(dy):,.2f} assumed target over {len(dy)} days")
