"""Generate the SYNTHETIC advertising dataset used in this case study.

All values are invented. The dataset reproduces the *structure* and the
*types of data-quality issues* seen in a real-world advertising export
(zero-spend revenue, a tiny-spend outlier week, a combined account field,
a repeated budget value, uneven account-by-date coverage), but none of the
numbers, account identifiers or dates come from any company's data.
"""
import csv
import datetime as dt
import random

random.seed(2026)

START = dt.date(2026, 10, 1)
N_DAYS = 25  # 1 Oct - 25 Oct 2026
BUDGET = 15000  # repeated on every row, like the source export

# Dates with no recorded spend at all
ZERO_SPEND_DATES = {dt.date(2026, 10, d) for d in (1, 2, 3, 4, 9, 10, 11)}
# Reported revenue on some zero-spend dates (attribution lag / tracking gap)
ZERO_SPEND_REVENUE = {
    dt.date(2026, 10, 2): ("ACC-B", 1180.40),
    dt.date(2026, 10, 3): ("ACC-C", 960.25),
    dt.date(2026, 10, 10): ("ACC-B", 640.80),
    dt.date(2026, 10, 11): ("ACC-D", 355.10),
}
# One tiny-spend day with large reported revenue (the first-week outlier)
OUTLIER_DAY = dt.date(2026, 10, 4)
LOW_ROAS_DAY = dt.date(2026, 10, 17)
COMBINED_DAY = dt.date(2026, 10, 14)

ACCOUNT_SHARE = {"ACC-A": 0.66, "ACC-B": 0.14, "ACC-C": 0.10, "ACC-D": 0.06, "ACC-E": 0.04}
COVERAGE = {"ACC-A": 1.0, "ACC-B": 0.7, "ACC-C": 0.5, "ACC-D": 0.4, "ACC-E": 0.3}


def week_start(d):
    return d - dt.timedelta(days=d.weekday())


def daily_spend_target(d):
    ws = week_start(d)
    if ws == dt.date(2026, 10, 5):
        return random.uniform(360, 440)
    if ws == dt.date(2026, 10, 12):
        return random.uniform(880, 980)
    return random.uniform(640, 760)


def account_roas(acct, d):
    ws = week_start(d)
    if acct == "ACC-A":
        base = {dt.date(2026, 10, 5): 3.7, dt.date(2026, 10, 12): 2.3}.get(ws, 2.2)
        return base * random.uniform(0.9, 1.1)
    return random.uniform(5.0, 9.5)


rows = []
for i in range(N_DAYS):
    d = START + dt.timedelta(days=i)

    if d in ZERO_SPEND_DATES:
        if d == OUTLIER_DAY:
            rows.append((d, "ACC-A", 9.60, 2840.00))
        if d in ZERO_SPEND_REVENUE:
            acct, rev = ZERO_SPEND_REVENUE[d]
            rows.append((d, acct, 0.00, rev))
        elif d != OUTLIER_DAY:
            # A date that exists in the export but with nothing recorded
            rows.append((d, "ACC-A", 0.00, 0.00))
        continue

    total = daily_spend_target(d)
    if d == LOW_ROAS_DAY:
        total = 1040.0
    for acct, share in ACCOUNT_SHARE.items():
        if random.random() > COVERAGE[acct]:
            continue
        spend = round(total * share * random.uniform(0.85, 1.15), 2)
        roas = account_roas(acct, d)
        if d == LOW_ROAS_DAY:
            roas *= 0.12
        rows.append((d, acct, spend, round(spend * roas, 2)))

    if d == COMBINED_DAY:
        # An unresolved record where two accounts share one field
        rows.append((d, "ACC-C, ACC-D", 640.00, 1310.00))

rows.sort(key=lambda r: (r[0], r[1]))
with open("synthetic_ad_data.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "account_id", "ad_spend", "reported_revenue", "budget"])
    for d, acct, spend, rev in rows:
        w.writerow([d.isoformat(), acct, f"{spend:.2f}", f"{rev:.2f}", BUDGET])

print(f"Wrote {len(rows)} rows")
