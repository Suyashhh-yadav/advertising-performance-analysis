# Analysis Framework

## 1. Establish the grain

The demonstration CSV is designed at one row per date × account × campaign. Validate this key before aggregating. If the source system uses a different grain, document it and adapt the model.

## 2. Establish the baseline

Calculate total spend, reported revenue, and blended ROAS. Use a ratio of totals:

`Blended ROAS = Total Reported Revenue / Total Spend`

Do not average daily ROAS values to calculate the overall result. Daily ratios have different spend weights.

## 3. Analyse trends

Compare daily and weekly spend, revenue, and ROAS. Use a consistent week-start convention. Look for changes in efficiency, but do not claim that spend changes caused revenue or ROAS changes.

## 4. Analyse allocation

Rank accounts and campaigns by spend. Show spend share alongside ROAS and absolute spend. A high ROAS on very low spend is a signal for validation or a controlled test—not automatic evidence to scale.

## 5. Review pacing

Compare actual spend with a budget reference only after confirming its scope and grain (daily, campaign, account, or monthly). Never sum a repeated budget field across fact rows.

## 6. Investigate exceptions

Examples include:
- Revenue recorded when spend is zero.
- Spend or revenue values outside expected ranges.
- Missing dates or missing account-campaign combinations.
- Duplicate date-account-campaign keys.
- Unusually high ROAS caused by a very small denominator.
- Ambiguous identifiers or inconsistent naming.

## 7. Convert analysis into decisions

For each finding, document:
- **Evidence:** the metric or record supporting the observation.
- **Interpretation:** what the evidence may indicate.
- **Limitation:** what is not known.
- **Next step:** the smallest useful investigation or test.
- **Success measure:** what should change if the action is effective.

Recommendations should not imply that a business outcome has already been achieved.
