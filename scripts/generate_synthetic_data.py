"""Generate a fictional advertising performance dataset for this portfolio.

The output is synthetic and is not derived from any employer or assessment data.
Run from the repository root:
    python scripts/generate_synthetic_data.py
"""
from datetime import date, timedelta
from pathlib import Path
import csv
import random

SEED = 20261116
START_DATE = date(2026, 9, 1)
DAYS = 30
ACCOUNTS = {
    "Account A": ["Campaign A1", "Campaign A2"],
    "Account B": ["Campaign B1", "Campaign B2"],
    "Account C": ["Campaign C1", "Campaign C2"],
}

def main():
    rng = random.Random(SEED)
    output = Path(__file__).resolve().parents[1] / "data" / "synthetic_ad_performance.csv"
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for day_index in range(DAYS):
        current_date = START_DATE + timedelta(days=day_index)
        for account, campaigns in ACCOUNTS.items():
            for campaign in campaigns:
                # Deterministic activity pattern with occasional zero-spend days.
                active = rng.random() > 0.10
                spend = round(rng.uniform(18, 145), 2) if active else 0.0
                # Synthetic revenue with noise; not intended as a benchmark.
                efficiency = rng.uniform(1.1, 4.2)
                revenue = round(spend * efficiency + rng.uniform(0, 35), 2)
                if spend == 0 and rng.random() < 0.45:
                    revenue = round(rng.uniform(0, 55), 2)
                elif spend == 0:
                    revenue = 0.0

                rows.append({
                    "Date": current_date.isoformat(),
                    "Account": account,
                    "Campaign": campaign,
                    "Spend": f"{spend:.2f}",
                    "Revenue": f"{revenue:.2f}",
                    "Budget": "100.00",
                })

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["Date", "Account", "Campaign", "Spend", "Revenue", "Budget"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} synthetic rows to {output}")

if __name__ == "__main__":
    main()
