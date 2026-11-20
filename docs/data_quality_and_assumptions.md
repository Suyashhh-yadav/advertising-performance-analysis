# Data Quality and Assumptions

## Validation checklist

| Check | Why it matters | Expected treatment |
|---|---|---|
| Data types | Text-formatted numbers break calculations | Convert to appropriate numeric/date types |
| Duplicate grain keys | Can inflate spend and revenue | Investigate before removing |
| Missing dates | Can make trends appear incomplete | Distinguish no activity from missing data |
| Missing account/campaign labels | Prevents reliable attribution | Preserve and flag unknown values |
| Zero spend with revenue | ROAS is undefined for the row/period | Keep revenue; return blank ROAS when spend is zero |
| Extreme ROAS | Small denominators can create misleading ratios | Show spend and revenue beside ROAS |
| Repeated budget values | Summing repeated targets inflates budget | Confirm budget grain; use a non-additive measure where appropriate |
| Ambiguous account mapping | Allocation would be speculative | Keep unresolved and investigate |

## Assumptions policy

Any assumption needed to make a calculation must be visible in the report. Examples:
- The definition of revenue and its attribution window.
- Whether spend is net or gross of fees and credits.
- Whether budget is daily, monthly, account-level, or campaign-level.
- Whether a missing row means zero activity or missing data.
- The reporting time zone and week-start convention.

Do not silently convert an assumption into a fact.

## Metric limitations

ROAS compares reported revenue with ad spend. It does not account for margin, refunds, fulfilment, overhead, or incrementality. It should not be described as profit, ROI, or proof of causal impact.
