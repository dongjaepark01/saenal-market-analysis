import pandas as pd
import numpy as np

df = pd.read_pickle('df_products.pkl')
print('df shape', df.shape)
print(df['Product'].nunique(), 'unique product names out of', len(df), 'rows')

# how many years does each product appear in?
appear = df.groupby('Product')['Year'].agg(['nunique', 'max', 'min'])
print(appear['nunique'].value_counts())

# Aggregate to SKU level across years (this dataset has no customer ID, so we
# apply RFM logic to products/SKUs instead of customers)
sku = (
    df.groupby('Product')
    .agg(
        Frequency = ('Num. Order', 'sum'),
        Monetary  = ('Revenues', 'sum'),
        Last_Year = ('Year', 'max'),
        Category  = ('Category', 'first'),
        Company   = ('Company', 'first'),
    )
    .reset_index()
)
print(sku.shape)

LATEST_YEAR = df['Year'].max()
sku['Recency_Years'] = LATEST_YEAR - sku['Last_Year']  # 0 = active in latest year

# R score: fewer years since last active = higher score
sku['R_Score'] = sku['Recency_Years'].map({0:5, 1:3, 2:2, 3:1}).fillna(1).astype(int)

# F, M scores via quantile rank (1-5), handling duplicate edges
def qscore(s, ascending=True):
    ranks = s.rank(method='first', ascending=ascending)
    return pd.qcut(ranks, 5, labels=[1,2,3,4,5]).astype(int)

sku['F_Score'] = qscore(sku['Frequency'])
sku['M_Score'] = qscore(sku['Monetary'])
sku['RFM_Sum'] = sku['R_Score'] + sku['F_Score'] + sku['M_Score']

def segment(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    if r >= 4 and f >= 4 and m >= 4:
        return 'Star Performers'
    if r <= 2 and f >= 4 and m >= 4:
        return 'Declining Stars (At Risk)'
    if r >= 4 and f <= 2 and m <= 2:
        return 'New / Niche SKUs'
    if r <= 2 and f <= 2 and m <= 2:
        return 'Dormant / Long-tail'
    if f >= 3 and m >= 3:
        return 'Steady Sellers'
    return 'Needs Review'

sku['Segment'] = sku.apply(segment, axis=1)

print(sku['Segment'].value_counts())
print()
seg_summary = sku.groupby('Segment').agg(
    SKUs=('Product','count'),
    Total_Revenue=('Monetary','sum'),
    Avg_Revenue=('Monetary','mean'),
    Avg_Orders=('Frequency','mean'),
).sort_values('Total_Revenue', ascending=False)
seg_summary['Revenue_Share_%'] = (seg_summary['Total_Revenue'] / seg_summary['Total_Revenue'].sum() * 100).round(1)
print(seg_summary)

sku.to_pickle('sku_rfm.pkl')
seg_summary.to_pickle('rfm_seg_summary.pkl')
print('\nSaved sku_rfm.pkl, rfm_seg_summary.pkl')
