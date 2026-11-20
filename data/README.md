# Data

The CSV in this folder is synthetic demonstration data created by `scripts/generate_synthetic_data.py`.

- It is not sourced from a real advertiser or employer.
- Account and campaign labels are fictional.
- Values are generated for portfolio demonstration only.
- Do not interpret the values as benchmarks or actual business results.

To regenerate:

```bash
python scripts/generate_synthetic_data.py
```

The dataset grain is one row per **date × account × campaign**. `Budget` is defined at this same campaign-day grain in this synthetic example, so it can be summed across those rows. This is a deliberate modelling choice for the demo, not a claim about any real advertiser dataset.
