import pandas as pd
import numpy as np

df = pd.read_pickle('df_products.pkl')

# Use 2022 and 2023 (both full calendar years) for a clean YoY comparison
cat_yearly = df.groupby(['Category', 'Year']).agg(
    Revenue=('Revenues', 'sum'),
    Orders=('Num. Order', 'sum'),
    SKUs=('Product', 'nunique'),
    Refund_Rate=('Refund Rate', 'mean'),
).reset_index()

rev_2022 = cat_yearly[cat_yearly.Year==2022].set_index('Category')['Revenue']
rev_2023 = cat_yearly[cat_yearly.Year==2023].set_index('Category')['Revenue']

cat_2023 = cat_yearly[cat_yearly.Year==2023].set_index('Category').copy()
cat_2023['Revenue_2022'] = rev_2022
cat_2023['YoY_Growth_%'] = ((cat_2023['Revenue'] - cat_2023['Revenue_2022']) / cat_2023['Revenue_2022'] * 100)
cat_2023['Revenue_Share_%'] = cat_2023['Revenue'] / cat_2023['Revenue'].sum() * 100
cat_2023 = cat_2023.dropna(subset=['YoY_Growth_%'])  # need both years present
cat_2023 = cat_2023[cat_2023['Revenue_2022'] > 0]

# 'Unknown' is a data-quality artifact (unmatched product-category merges), not
# a real merchandising category -- exclude it from the strategic matrix, same
# treatment the v2 report gave it in the discount-segment analysis.
cat_2023_known = cat_2023[cat_2023.index != 'Unknown'].copy()
cat_2023_known['Revenue_Share_%'] = cat_2023_known['Revenue'] / cat_2023_known['Revenue'].sum() * 100

# Clip extreme growth outliers for plotting readability, keep raw in table
cat_2023 = cat_2023.sort_values('Revenue', ascending=False)
cat_2023_known = cat_2023_known.sort_values('Revenue', ascending=False)

print(cat_2023[['Revenue','Revenue_2022','YoY_Growth_%','Revenue_Share_%','Orders','SKUs','Refund_Rate']].round(2).head(40))
print('\nTotal categories analyzed:', len(cat_2023))

# Quadrant assignment (BCG-style growth-share matrix), computed on known categories only
share_thresh = cat_2023_known['Revenue_Share_%'].mean()
growth_thresh = 0  # growth vs decline is the natural business cutoff

def quadrant(row):
    high_share = row['Revenue_Share_%'] >= share_thresh
    high_growth = row['YoY_Growth_%'] >= growth_thresh
    if high_share and high_growth:
        return 'Star'
    if high_share and not high_growth:
        return 'Cash Cow'
    if not high_share and high_growth:
        return 'Question Mark'
    return 'Dog'

cat_2023_known['Quadrant'] = cat_2023_known.apply(quadrant, axis=1)
print('\n', cat_2023_known['Quadrant'].value_counts())
print('\nShare threshold:', share_thresh, 'Growth threshold:', growth_thresh)
print('\nTop rows:')
print(cat_2023_known[['Revenue','YoY_Growth_%','Revenue_Share_%','Quadrant']].head(12).round(1))

cat_2023.to_pickle('category_matrix_all.pkl')       # includes Unknown, for reference
cat_2023_known.to_pickle('category_matrix.pkl')     # excludes Unknown, used for chart/report
print('\nSaved category_matrix.pkl / category_matrix_all.pkl')
