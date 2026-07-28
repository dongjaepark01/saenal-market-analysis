import pandas as pd
import numpy as np

df = pd.read_pickle('df_products.pkl')

def hhi_cr(series_share_pct):
    """series_share_pct: shares in percent (0-100), summing to ~100."""
    hhi = (series_share_pct**2).sum()  # HHI on 0-10000 scale when shares are in %
    cr4 = series_share_pct.sort_values(ascending=False).head(4).sum()
    return hhi, cr4

def concentration_report(dfx, value_col, label):
    vend = dfx[dfx['Company'] != 'Unknown'].groupby('Company')[value_col].sum().sort_values(ascending=False)
    share = vend / vend.sum() * 100
    hhi, cr4 = hhi_cr(share)
    print(f'--- {label} (by {value_col}) ---')
    print('N vendors:', len(vend))
    print('Top 5 share (%):')
    print(share.head(5).round(2))
    print(f'HHI: {hhi:.0f}  (0-10000 scale; >2500=highly concentrated, 1500-2500=moderate, <1500=competitive)')
    print(f'CR4 (top-4 share): {cr4:.1f}%')
    print()
    return vend, share, hhi, cr4

print('=== Overall (all years pooled) ===')
vend_rev, share_rev, hhi_rev, cr4_rev = concentration_report(df, 'Revenues', 'Revenue')
vend_ord, share_ord, hhi_ord, cr4_ord = concentration_report(df, 'Num. Order', 'Order volume')

# Listing count (SKU count) concentration -- comparable to the v2 report's "frequency of companies" chart
listing_count = df[df['Company']!='Unknown'].groupby('Company')['Product'].nunique().sort_values(ascending=False)
listing_share = listing_count / listing_count.sum() * 100
hhi_listing, cr4_listing = hhi_cr(listing_share)
print('--- Listing count (SKU count) ---')
print(listing_count.head(5))
print(f'HHI: {hhi_listing:.0f}   CR4: {cr4_listing:.1f}%')
print()

# By year, to see if concentration is rising or falling over time
print('=== HHI trend by year (revenue-based) ===')
yearly_hhi = {}
for yr, g in df[df['Company']!='Unknown'].groupby('Year'):
    v = g.groupby('Company')['Revenues'].sum()
    s = v / v.sum() * 100
    h, c4 = hhi_cr(s)
    yearly_hhi[yr] = {'HHI': h, 'CR4': c4, 'N_vendors': v[v>0].shape[0]}
yearly_hhi_df = pd.DataFrame(yearly_hhi).T
print(yearly_hhi_df.round(1))

# Category revenue exposure of the #1 vendor (checks the report's "cap at 20% of category revenue" recommendation)
top_vendor = vend_rev.index[0]
print(f'\nTop vendor: {top_vendor}')
cat_share = df.groupby('Category').apply(
    lambda g: g[g.Company==top_vendor]['Revenues'].sum() / g['Revenues'].sum() * 100 if g['Revenues'].sum()>0 else 0
).sort_values(ascending=False)
print(f'{top_vendor} share of category revenue (top 8 categories where present):')
print(cat_share.head(8).round(1))

# v2 report used raw row-count ("listing frequency" across yearly snapshots) as
# its vendor concentration proxy. Reproduce it for continuity, then show why it
# understates the real risk: it conflates a vendor's tenure/listing persistence
# with its actual economic weight.
row_count = df[df['Company']!='Unknown']['Company'].value_counts()
row_share = row_count / row_count.sum() * 100
hhi_row, cr4_row = hhi_cr(row_share)
print('=== Legacy "listing frequency" metric (row count, v2 methodology) ===')
print(row_count.head(5))
print(f'HHI: {hhi_row:.0f}   CR4: {cr4_row:.1f}%  <- looks competitive, but is misleading\n')

print('=== Comparison ===')
print(f'{"Metric":<28}{"Top vendor":<12}{"Top share":>10}{"HHI":>8}{"CR4":>8}')
print(f'{"Listing frequency (v2)":<28}{row_share.idxmax():<12}{row_share.max():>9.1f}%{hhi_row:>8.0f}{cr4_row:>7.1f}%')
print(f'{"Unique SKU count":<28}{listing_share.idxmax():<12}{listing_share.max():>9.1f}%{hhi_listing:>8.0f}{cr4_listing:>7.1f}%')
print(f'{"Order volume":<28}{share_ord.idxmax():<12}{share_ord.max():>9.1f}%{hhi_ord:>8.0f}{cr4_ord:>7.1f}%')
print(f'{"Revenue (economic weight)":<28}{share_rev.idxmax():<12}{share_rev.max():>9.1f}%{hhi_rev:>8.0f}{cr4_rev:>7.1f}%')

import pickle
with open('vendor_concentration.pkl', 'wb') as f:
    pickle.dump({
        'vend_rev': vend_rev, 'share_rev': share_rev, 'hhi_rev': hhi_rev, 'cr4_rev': cr4_rev,
        'listing_count': listing_count, 'listing_share': listing_share,
        'hhi_listing': hhi_listing, 'cr4_listing': cr4_listing,
        'yearly_hhi_df': yearly_hhi_df,
        'top_vendor': top_vendor, 'cat_share': cat_share,
        'row_count': row_count, 'row_share': row_share, 'hhi_row': hhi_row, 'cr4_row': cr4_row,
    }, f)
print('\nSaved vendor_concentration.pkl')
