# SAENAL Market — Sales Analysis & Forecast (v3)

A data analysis project from my internship at SAENAL Market, a Korean online food and health marketplace.
The goal was to turn raw transactional exports into decisions a small analytics/merchandising team can act
on — not just descriptive charts. This v3 update extends the original 4-question EDA + forecast with four
analyses aimed squarely at retail/e-commerce decision-making: SKU-level RFM segmentation, a category
profitability matrix, a benchmarked forecast model choice, and a quantified vendor-risk assessment.

---

## What I Did

The business had 3+ years of sales data but no structured way to make sense of it. I built an end-to-end
analysis pipeline that answers eight questions across four areas:

**Revenue & demand**
1. Where is revenue coming from — which categories, vendors, and customer segments drive the most sales?
2. Is there a seasonal pattern, and is the business capitalizing on it?

**Customers & loyalty**
3. Is the loyalty program actually working?
4. Which SKUs deserve inventory priority, and which are quietly losing relevance? *(new — RFM)*

**Portfolio & risk**
5. Which categories are genuinely profitable growth engines vs. cash cows, on a like-for-like basis? *(new — growth-share matrix)*
6. How concentrated is supplier risk, in numbers a risk committee would accept? *(new — HHI/CR4)*

**Forecasting**
7. What does the next 12 months look like?
8. Is the forecasting model actually the right choice, or just convention? *(new — SARIMA vs. Prophet benchmark)*

---

## Key Findings

- **Health category dominance, now with a second engine** — 건강 grew from near-zero to the #1 revenue
  driver within 18 months (+177% YoY in the latest full-year comparison). A data-quality fix during this
  update also revealed that 건강식품 — previously miscounted as declining 74% YoY — is actually a stable,
  comparably-sized second Star (+4.7% YoY) once a mislabeled ₩900M+ SKU was correctly reclassified.
- **The product portfolio follows a sharp Pareto curve** — SKU-level RFM segmentation shows ~12% of SKUs
  ("Star Performers") generate 51% of revenue, while a 196-SKU "Declining Stars" segment (23% of historical
  revenue) has gone quiet in the last 2+ years — a concrete, bounded triage list rather than a vague
  long-tail problem.
- **Vendor concentration is worse than a listing-count chart suggests** — by number of catalog listings the
  platform looks diversified (HHI 128, "competitive"). By revenue — the metric that actually determines
  supply risk — the top vendor holds 21.8% of platform revenue and 78% of the 건강식품 category, both above
  a 20% single-vendor exposure guideline.
- **SARIMA beats Prophet on this dataset, and now I can prove it** — a held-out accuracy test (last 6
  months) gives SARIMA a 23.9% MAPE vs. Prophet's 41.0%. With only ~2.5 years of history and a strong
  regular seasonal cycle, SARIMA's explicit seasonal order outperforms Prophet's changepoint-based trend
  model, which needs more history to earn its flexibility.
- **Loyalty program ROI** — member customers generate ~5–6× more revenue than non-members, suggesting the
  program changes purchasing behavior, not just discount usage.
- **Predictable seasonality** — December, June, and November consistently peak every year; July–August is
  always the trough (~50% below peak).
- **Price doesn't drive revenue** — correlation between avg. product price and revenue is only r=0.23;
  brand trust and perceived value matter more.

---

## Analysis Breakdown

### Data Preprocessing
- Merged product, sales, and category data across 4 years (2021–2024)
- Standardized inconsistent product naming using keyword-matching
- Extracted company names from product name patterns like `[CompanyName] Product`
- Removed deprecated categories (CATE88, CATE40, CATE0) after confirming with the business
- Imputed missing category and company fields using per-company mode values
- **New:** stripped hidden non-breaking-space characters from `Category`/`Company`/`Discount Target` labels
  that silently broke exact-match filtering (though not `groupby`, which is why v2 didn't catch it)
- **New:** found and fixed a bracket-extraction bug where a promotional milestone SKU
  (`[아임굿 1st 원데이 이벤트 ...]`) was miscounted as its own vendor — a ~₩930M chunk that also cascaded
  into a category-mislabeling issue (see below)

### Exploratory Data Analysis (EDA)
- Revenue trend analysis: annual YoY comparison + monthly seasonality breakdown
- Category-level revenue decomposition across all years
- Top 10 products by total revenue; top 20 vendors by listing count
- Discount application analysis: member vs. non-member revenue split
- Correlation heatmap and pairplot across key variables

### SKU-Level RFM Segmentation *(new)*
- Classic RFM segments customers, but this dataset has no customer ID at any grain — only daily-aggregate
  sales and yearly product snapshots. Adapted the same Recency/Frequency/Monetary logic to the SKU level
  instead of forcing a customer segmentation the data can't support.
- Six portfolio segments (Star Performers, Declining Stars, Steady Sellers, Needs Review, Dormant/Long-tail,
  New/Niche), each scored 1–5 on R/F/M and mapped to a merchandising action.

### Category Profitability Matrix *(new)*
- No COGS/margin data exists at the product level, so built a BCG-style growth-share matrix as a
  profitability proxy: YoY revenue growth (2022→2023) vs. revenue share, bubble-sized by order volume.
- Surfaced and explained a real discrepancy with the original qualitative claim about 건강식품's growth
  trend, traced to the preprocessing bug above.

### Vendor Concentration Quantification *(new)*
- Replaced the original's listing-frequency bar chart with the Herfindahl-Hirschman Index (HHI) and top-4
  concentration ratio (CR4), computed across four bases (listing frequency, unique SKU count, order volume,
  revenue) to show how differently "concentration" looks depending on what you measure.
- Tracked HHI year-over-year to show concentration is trending up, not just a static risk.

### Revenue Forecasting
- Benchmarked **SARIMA(1,1,1)(1,1,1,12)** against **Prophet** on a proper train/test split (last 6 full
  months held out), scoring both on MAE, RMSE, and MAPE before committing to a production model.
- Refit the winning model (SARIMA) on the complete history for the actual 12-month forecast with 95%
  confidence intervals.

---

## Tools & Methods

| Area | Stack |
|---|---|
| Language | Python |
| Data manipulation | pandas, numpy |
| Visualization | matplotlib, seaborn |
| Forecasting | statsmodels (SARIMA), prophet |
| Segmentation | Custom RFM scoring (pandas `qcut`) |
| Concentration metrics | Herfindahl-Hirschman Index, CR4 (custom implementation) |
| Data source | Excel files (multi-year, multi-table) |
| Export | CSV (Tableau-ready) |

---

## File Structure

```
├── SAENAL_Analysis_v3.ipynb        # Main analysis notebook (executed, with real outputs)
├── SAENAL_Report_v3.pdf            # Full write-up: EDA, RFM, category matrix, forecast comparison, vendor risk
├── tableau_products.csv            # Product-level data (Tableau)
├── tableau_monthly_revenue.csv     # Monthly revenue time series (Tableau)
├── tableau_category_revenue.csv    # Revenue by year × category (Tableau)
├── tableau_category_matrix.csv     # Category growth-share matrix data (Tableau)
├── tableau_discount_revenue.csv    # Revenue by discount type (Tableau)
├── tableau_sku_rfm.csv             # SKU-level RFM scores and segments (Tableau)
├── tableau_vendor_concentration.csv# HHI/CR4 by concentration basis (Tableau)
├── tableau_model_comparison.csv    # SARIMA vs. Prophet accuracy metrics (Tableau)
├── tableau_forecast.csv            # SARIMA forecast + 95% CI (Tableau)
├── tableau_combined_revenue.csv    # Actual + forecast combined series (Tableau)
└── README.md
```

---

## Business Recommendations

1. **Accelerate loyalty enrollment** — converting 15% of non-members to membership status could generate
   an estimated ₩280–420M in incremental revenue
2. **Double down on 건강 / 건강식품** — both confirmed Stars with no saturation signal
3. **Formalize a seasonal campaign calendar** — pre-plan June/November/December pushes; counter-program the
   July–August trough
4. **Audit and reactivate the "Declining Stars" SKU segment** *(new)* — 196 SKUs holding 23% of historical
   revenue have gone quiet; check stock and placement before writing this off as churn
5. **Cap single-vendor exposure, starting with 아임굿** *(new)* — currently 78% of the 건강식품 category
   and 21.8% of platform revenue sit with one vendor
6. **Standardize data infrastructure** — mandate membership capture at checkout and consistent product
   naming; automate a check on the "Unknown" bucket's size given how much one mislabeled SKU can distort
   category-level conclusions
7. **Recalibrate the forecast model quarterly** *(new)* — re-run the SARIMA vs. Prophet benchmark as more
   data accumulates rather than treating the model choice as permanent

---

## Data Note

Raw data files are not included in this repository as they contain proprietary business information. The
notebook is structured to run with the original Excel files if available. All figures in this README and
the accompanying report were computed directly from those files.
