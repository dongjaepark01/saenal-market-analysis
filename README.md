# SAENAL Market — Sales Analytics and Forecasting

Sales analysis completed during my Data Analytics internship at SAENAL Market (June–December 2024). This repository presents the public report; the report was subsequently organized and corrected for portfolio presentation.

## Public report

- [PDF report](public/SAENAL_Report_Public.pdf)
- [HTML report](public/SAENAL_Report_Public.html) — download the `public/` folder together to retain its chart images.

The public edition replaces monetary amounts with indices and anonymizes supplier and campaign identifiers. It retains selected aggregate counts, percentages, and model evaluation metrics.

## Analysis

- Prepared 5,400+ product and daily sales records with Python/pandas, standardizing product names, joining category reference tables, and resolving missing vendor and category labels.
- Built Tableau dashboards covering monthly revenue, category performance, and saved 12-month revenue forecasts for sales review and planning.
- Segmented 2,100+ products into six groups using product-level RFM analysis, flagging 196 products absent from later product snapshots that represented 23.3% of historical product revenue for inventory and merchandising review.
- Compared SARIMA and Prophet on a six-month holdout using MAE, RMSE, and MAPE; SARIMA achieved 23.9% MAPE versus Prophet’s 41.0%.
- Examined category performance, discount-label distribution, price–revenue relationships, and supplier concentration to develop seven business recommendations.

## Interpretation and timing

All seven recommendations were proposed during the internship. Their adoption and subsequent business outcomes were not verified. Later report revisions document and clarify the internship work rather than establish a new recommendation date.

RFM segments describe products, not customers. Absence from later product snapshots does not prove zero subsequent sales. Category revenue analysis does not establish profitability without cost data, and correlations do not demonstrate causal effects.

The holdout comparison and saved forecast use different fitting setups. The saved forecast includes a partial final month and has wide confidence intervals, including negative lower bounds; it is a planning reference rather than a validated business outcome. Details are documented in the report.

## Local organization

```text
SAENAL/
├── README.md
├── .gitignore
├── public/      # Public HTML, PDF, and the 14 referenced chart images
└── private/     # Local-only original analysis workspace and internal report
```

The original notebook, source scripts, raw exports, intermediate data, chart files, previous README, and internal report are retained in `private/`. Run the existing analysis scripts from that directory so their relative input paths continue to resolve. The original public report files also remain there as working outputs; `public/` contains the curated export copy.

Only the public export and repository documentation are included in this cleanup commit. Files previously committed can still exist in older Git history; ignoring or removing them from the current version does not erase that history.
