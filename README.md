# Advertising Performance Analysis: From Data to Business Decisions

> A business case study in analyzing advertising performance, evaluating budget efficiency, identifying data-quality limitations, and translating findings into recommendations.

**Tools:** Power BI · DAX · Power Query · Python (verification)
**Focus:** Business analysis · Analytical judgment · Data quality · Decision support

> **All data in this repository is synthetic.** The method follows a real-world advertising assessment I completed, but every number, date and account identifier here was invented. Nothing comes from any company's data, and nothing here should be read as a result achieved for a real business. See [Data disclosure](#9-data-disclosure).

---

## How to read this project

| Label | Meaning |
|---|---|
| **Fact** | A value calculated directly from the dataset |
| **Assumption** | An interpretation used because the data did not define it |
| **Hypothesis** | A possible explanation that has not been verified |
| **Recommendation** | A proposed action to investigate; not a proven outcome |

## Repository contents

| File | Purpose |
|---|---|
| `synthetic_ad_data.csv` | The synthetic dataset (55 rows, 1-25 Oct 2026) |
| `generate_data.py` | Seeded generator, so the dataset is reproducible |
| `analysis.py` | Recomputes every figure quoted below |

---

## 1. Business problem

The dataset contains advertising spend, reported revenue, dates, account identifiers and a budget field. The business questions were:

- How much was spent, and how much revenue was reported?
- How did ROAS change over time?
- How was spend distributed across accounts?
- Were there days with weak or unusual reported performance?
- How did daily spend compare with a provisional budget target?
- Which data-quality limitations must be resolved before making budget decisions?

The goal is a performance overview and decision-support recommendations, not a claim that the analysis improved campaign results.

## 2. Data preparation and analytical approach

- Reviewed fields, date coverage, spend, revenue, budget and account identifiers.
- Prepared date and numeric fields in Power Query; built a date table related to the advertising data.
- Built DAX measures for total spend, reported revenue, ROAS and daily performance status.
- Compared performance by day, week and account.
- Reviewed unusual values and documented assumptions and limitations.
- Cross-checked every headline figure with `analysis.py`.

Weeks start on Monday. The first weekly period is labelled **week of 28 Sep 2026** and contains only the four available records for 1-4 Oct.

## 3. Key findings (synthetic data)

| Analysis | Finding | Business relevance |
|---|---|---|
| Overall | **$11,714.25** spend, **$43,168.63** reported revenue, blended ROAS **3.69x** | Reported return baseline |
| Weekly trend | ROAS fell from **5.08x** (week of 5 Oct) to **2.79x** (week of 12 Oct), then recovered to **3.45x** (week of 19 Oct) | Efficiency weakened as spend rose, then partly recovered as it fell |
| Account concentration | `ACC-A` took **$8,773.71**, **74.9%** of spend, at **2.65x** ROAS | Overall results depend heavily on one account |
| Small accounts | Four small accounts took **19.6%** of spend but reported **43.0%** of revenue | High ROAS on little spend; needs validation before any scaling |
| Daily | **17 Oct**: $802.52 spend, $351.50 revenue, **0.44x** ROAS | A day to investigate at campaign level |
| Zero-spend dates | **6** dates had zero spend; **$3,136.55** (7.3%) of reported revenue sits on them | Attribution or recording problem to validate |
| First weekly period | **518.8x** ROAS on **$9.60** spend | Low-spend outlier that distorts the weekly chart scale |

ROAS is total reported revenue divided by total ad spend in the current filter context. Blended ROAS is a ratio of totals, not an average of daily or account ROAS values.

## 4. Analysis and business interpretation

### 4.1 Weekly efficiency trend

- **Business question:** Did reported efficiency hold as spend increased?
- **Evidence (fact):** Week of 5 Oct: $1,224.27 spend, $6,214.42 revenue, 5.08x. Week of 12 Oct: $6,340.17 spend, $17,678.11 revenue, 2.79x. Week of 19 Oct: $4,140.21 spend, $14,295.45 revenue, 3.45x.
- **Interpretation:** Spend rose about 5.2x between the first two weeks while revenue rose about 2.8x, so ROAS fell. When spend dropped the following week, ROAS rose again.
- **Caution on comparability:** The week of 5 Oct had only 4 spending days (average $306.07 per spending day) against 7 in the week of 12 Oct ($905.74 per day). Part of the jump reflects more days running, not only higher daily intensity.
- **Recommendation:** Review campaign mix, targeting, audience quality and conversion performance before increasing budgets further.
- **Analytical limitation:** The pattern is *consistent with* diminishing returns, but the data cannot prove that higher spend caused the decline. Campaign changes, seasonality or attribution timing could also explain it (hypotheses).

### 4.2 Account-level spend concentration

- **Business question:** Where is the budget concentrated, and is it working?
- **Evidence (fact):** `ACC-A` recorded $8,773.71 spend (74.9% of total) at 2.65x ROAS.
- **Interpretation:** Overall performance is driven mainly by this account.
- **Recommendation:** Review its campaign-level results and test whether its spend is producing the expected incremental return. Consider budget changes only after that review.
- **Analytical limitation:** `ACC-B`, `ACC-C`, `ACC-D` and `ACC-E` show ROAS between 7.1x and 9.9x on small spend, and account-by-date coverage is unconfirmed (they appear on only 4 to 17 of 25 dates). Do not treat those ratios as scalable opportunities.

### 4.3 Low-ROAS day

- **Business question:** Which individual dates deserve closer review?
- **Evidence (fact):** On 17 Oct, spend was $802.52 and reported revenue $351.50 (0.44x). The next-lowest day was 2.69x.
- **Interpretation:** Reported revenue was well below ad spend, and the day stands apart from every other.
- **Hypotheses (unverified):** a campaign change, tracking gap or conversion lag.
- **Recommendation:** Review campaign, audience and conversion details for 17 Oct before adjusting any campaign or budget.

### 4.4 Budget pacing

- **Source field:** A $15,000 budget value repeated on every row. Its period and scope are not defined.
- **Assumption:** $15,000 is a monthly October budget spread evenly over 30 days, giving an **assumed $500 daily target**.
- **Evidence (fact, under that assumption):** Cumulative spend was $11,714.25 against $12,500.00 over 25 days (93.7%). On the 19 spending days, average spend was $616.54, with 14 days above $500 and 5 below.
- **Recommendation:** Confirm the budget period and allocation before treating variances as real over- or underspending.

## 5. Data quality findings and treatment

| Finding | Why it matters | Treatment |
|---|---|---|
| First-period ROAS of 518.8x | Tiny spend ($9.60) with $4,980.65 of reported revenue stretches the weekly chart | Retained and disclosed; not silently removed |
| Revenue on zero-spend dates | Daily ROAS is undefined; totals may include revenue with no matching spend | Kept in totals; daily ROAS left blank; flagged for validation |
| Combined account ID (`ACC-C, ACC-D`) | One record covers two accounts | Kept separate and unresolved; its $640.00 spend and $1,310.00 revenue were not allocated to either account |
| Repeated $15,000 budget value | Summing it would multiply the budget | Not summed; used only through the stated $500 assumption |
| Low-spend accounts with very high ROAS | Small denominators inflate ratios | Reported, but not used alone to justify budget increases |
| Unconfirmed account-by-date coverage | Accounts may be missing days | Account comparisons interpreted with this limitation |

### How much do the questionable records move the headline?

| Scenario | Blended ROAS |
|---|---|
| All reported revenue | **3.69x** |
| Excluding revenue on zero-spend dates | **3.42x** |
| Excluding the first (outlier) week | **3.26x** |
| Excluding both | **3.18x** |

The headline is sensitive to records that cannot be verified. A decision-maker should treat roughly **3.2x to 3.7x** as the plausible range until attribution is validated, rather than quoting 3.69x as fact.

## 6. Recommendations for stakeholders

1. **Investigate the weekly efficiency decline** at campaign, audience and conversion level before increasing spend.
2. **Review the highest-spend account** before changing its budget.
3. **Investigate 17 Oct** to understand why reported revenue was below spend.
4. **Validate attribution and spend recording** for revenue on zero-spend dates and the first-week outlier.
5. **Resolve the combined account record** and confirm account-by-date completeness before relying on account comparisons.
6. **Confirm the budget period and allocation** before using the assumed $500 daily target operationally.

These are recommendations based on the available data. This analysis does not show that they were implemented or produced a measured improvement.

## 7. Assumptions and metric definitions

- **ROAS:** Reported revenue divided by ad spend.
- **Blended ROAS:** Total reported revenue divided by total ad spend for the selected period.
- **Zero-spend days:** Daily ROAS is left blank, not treated as infinite or as above 1x.
- **Budget pacing:** $15,000 treated as a monthly budget at $500 per day. This is an assumption.
- **Profitability:** ROAS above 1x means reported revenue exceeds ad spend. It does not establish profitability because margins and other costs are unavailable.
- **Reported revenue:** Treated as reported; attribution has not been independently verified.

## 8. Dashboard and technical implementation

The Power BI report includes KPI cards (spend, reported revenue, blended ROAS, zero-spend days), a daily spend versus assumed-target view, weekly ROAS with a 1x benchmark and the outlier retained, a daily ROAS and status matrix, an account-level spend/revenue/ROAS matrix, date and account slicers, and documentation of assumptions and limitations.

**Technical components:** Power Query transformations, a date table and relationship, DAX measures, slicers and conditional formatting. `analysis.py` independently recomputes the figures in this document.


## 9. Data disclosure

This project follows the method of a company assessment I completed. The original dataset, instructions, screenshots and workbook are **not** included. The data here is entirely synthetic. It was generated by `generate_data.py` to reproduce the *structure* and the *kinds of data-quality issues* an advertising export can contain, using invented values and anonymized account labels. Findings and recommendations describe this synthetic dataset only and do not represent results for any real organization.

---

*Guiding principle: don't just show what happened. Explain what the data supports, what remains uncertain, why it matters, and what the business should investigate next.*
