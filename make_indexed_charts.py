"""
Regenerates every chart that shows absolute KRW figures as an indexed version
(2021 total annual revenue = index 100) for the public/anonymized report.
Reuses cached pickles from earlier steps -- no notebook re-execution, no model
refitting except one cheap SARIMA in-sample fit for the fit-validation chart.
"""
import warnings
warnings.filterwarnings('ignore')
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.font_manager as fm
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX

for _path in ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc']:
    try:
        fm.fontManager.addfont(_path)
    except Exception:
        pass
plt.rcParams.update({
    'font.family': 'Noto Sans CJK JP',
    'axes.unicode_minus': False,
    'figure.dpi': 120,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

df = pd.read_pickle('df_products.pkl')
monthly_ts = pd.read_pickle('monthly_ts.pkl')
with open('model_compare.pkl', 'rb') as f:
    mc = pickle.load(f)

# Single global index basis used everywhere: 2021 total annual revenue = 100
BASE_2021 = monthly_ts[monthly_ts['date'].dt.year == 2021]['total_revenue'].sum()
def idx(x):
    return x / BASE_2021 * 100

# ---------------------------------------------------------------------------
# 1. Revenue trends (monthly by year + annual totals) -> index
ts_df = monthly_ts.copy()
ts_df['year'] = ts_df['date'].dt.year
ts_df['month'] = ts_df['date'].dt.month
ts_df['idx'] = idx(ts_df['total_revenue'])
monthly_pivot_idx = ts_df.groupby(['year', 'month'])['idx'].sum().unstack('year')
yearly_idx = ts_df.groupby('year')['idx'].sum()

fig, axes = plt.subplots(1, 2, figsize=(16, 5))
monthly_pivot_idx.plot(ax=axes[0], marker='o', linewidth=2)
axes[0].set_title('Monthly Sales Trends (2021–2024)', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Revenue Index (2021 total = 100)')
axes[0].grid(alpha=0.3)
axes[0].legend(title='Year')

yearly_idx.plot(kind='bar', ax=axes[1], color='steelblue')
axes[1].set_title('Annual Sales Trends (2021–2024)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Revenue Index (2021 total = 100)')
axes[1].tick_params(axis='x', rotation=0)
for i, v in enumerate(yearly_idx.values):
    axes[1].text(i, v * 1.01, f'{v:.0f}', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('chart_revenue_trends_idx.png', dpi=150, bbox_inches='tight')
plt.close()
print('1/9 revenue_trends done')

# ---------------------------------------------------------------------------
# 2. Average monthly revenue -> index
MONTH_ORDER = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']
avg_monthly_idx = (
    monthly_ts.assign(month_name=lambda d: d['date'].dt.strftime('%B'), idx=lambda d: idx(d['total_revenue']))
    .groupby('month_name')['idx'].mean()
    .reindex(MONTH_ORDER[::-1])
)
fig, ax = plt.subplots(figsize=(9, 6))
avg_monthly_idx.plot(kind='barh', ax=ax, color='steelblue')
ax.set_title('Average Monthly Revenue Index (2021–2024)', fontsize=13, fontweight='bold')
ax.set_xlabel('Revenue Index (2021 total = 100, monthly average)')
plt.tight_layout()
plt.savefig('chart_avg_monthly_idx.png', dpi=150, bbox_inches='tight')
plt.close()
print('2/9 avg_monthly done')

# ---------------------------------------------------------------------------
# 3. Category revenue trend -> index
yearly_cat = df.groupby(['Year', 'Category'])['Revenues'].sum().reset_index()
yearly_cat['idx'] = idx(yearly_cat['Revenues'])
top5_cats = yearly_cat.groupby('Category')['Revenues'].sum().nlargest(5).index.tolist()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=yearly_cat, x='Year', y='idx', hue='Category', ax=ax, legend=False, linewidth=1.5)
last_year = yearly_cat['Year'].max()
for cat in top5_cats:
    sub = yearly_cat[(yearly_cat.Category == cat) & (yearly_cat.Year == last_year)]
    if not sub.empty:
        ax.annotate(cat, (last_year, sub['idx'].values[0]), fontsize=9, xytext=(5, 0), textcoords='offset points')
ax.set_ylabel('Revenue Index (2021 total = 100)')
ax.set_title('Revenue by Year and Category', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('chart_category_revenue_idx.png', dpi=150, bbox_inches='tight')
plt.close()
print('3/9 category_revenue done')

# ---------------------------------------------------------------------------
# 4. Discount/membership revenue -> % share (not index, cleaner here)
discount_rev = df.groupby('Discount Target')['Revenues'].sum().sort_values(ascending=False).reset_index()
discount_rev['share'] = discount_rev['Revenues'] / discount_rev['Revenues'].sum() * 100
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(x='Discount Target', y='share', data=discount_rev, palette='Blues_r', ax=ax)
for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.01,
            f'{bar.get_height():.1f}%', ha='center', fontsize=10)
ax.set_ylabel('% of total revenue')
ax.set_title('Revenue Share by Discount/Membership Segment', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('chart_discount_revenue_idx.png', dpi=150, bbox_inches='tight')
plt.close()
print('4/9 discount_revenue done')

# ---------------------------------------------------------------------------
# 5. Top 10 products by revenue -> index (only right panel needed; keep category freq panel too)
fig, axes = plt.subplots(1, 2, figsize=(18, 7))
cat_order = df['Category'].value_counts().index
sns.countplot(y='Category', data=df, order=cat_order, palette='Blues_r', ax=axes[0])
axes[0].set_title('Frequency of Categories', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Count')

top10 = df.groupby('Product')['Revenues'].sum().nlargest(10)
top10_idx = idx(top10)
top10_idx.plot(kind='barh', ax=axes[1], color='seagreen')
axes[1].invert_yaxis()
axes[1].set_title('Top 10 Products by Revenue Index', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Revenue Index (2021 total = 100)')
axes[1].set_yticklabels([lbl.get_text()[:28] + ('…' if len(lbl.get_text()) > 28 else '') for lbl in axes[1].get_yticklabels()])
plt.tight_layout()
plt.savefig('chart_category_top10_idx.png', dpi=150, bbox_inches='tight')
plt.close()
print('5/9 category_top10 done')

# ---------------------------------------------------------------------------
# 6. Seasonal decomposition -> on indexed series
ts_idx = monthly_ts.set_index('date')['total_revenue'].asfreq('ME')
ts_idx = idx(ts_idx)
decomp = seasonal_decompose(ts_idx, model='additive', period=12)
fig = decomp.plot()
fig.set_size_inches(12, 8)
fig.suptitle('Seasonal Decomposition of Revenue Index', fontsize=13, fontweight='bold')
for ax in fig.axes:
    ax.set_ylabel('Index')
plt.tight_layout()
plt.savefig('chart_decomposition_idx.png', dpi=150, bbox_inches='tight')
plt.close()
print('6/9 decomposition done')

# ---------------------------------------------------------------------------
# 7. SARIMA fit validation -> refit once on indexed full series (cheap, no Prophet)
ts_full_idx = idx(mc['ts_full'])
sarima_full_idx = SARIMAX(ts_full_idx, order=(1,1,1), seasonal_order=(1,1,1,12),
                           enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(ts_full_idx.index, ts_full_idx.values, label='Observed', linewidth=2, color='steelblue')
ax.plot(ts_full_idx.index, sarima_full_idx.fittedvalues, label='Fitted', linewidth=2, color='orange', linestyle='--')
ax.set_title('SARIMA Model Fit (Revenue Index)', fontsize=13, fontweight='bold')
ax.set_ylabel('Revenue Index (2021 total = 100)')
ax.legend()
plt.tight_layout()
plt.savefig('chart_sarima_fit_idx.png', dpi=150, bbox_inches='tight')
plt.close()
print('7/9 sarima_fit done')

# ---------------------------------------------------------------------------
# 8. 12-month forecast -> index (reuse cached forecast, just rescale)
fc_mean_idx = idx(mc['sarima_full_mean'])
fc_ci_idx = idx(mc['sarima_full_ci'])
fig, ax = plt.subplots(figsize=(13, 5))
ax.scatter(ts_full_idx.index, ts_full_idx.values, color='steelblue', s=20, zorder=3, label='Observed')
full_index = ts_full_idx.index.tolist() + fc_mean_idx.index.tolist()
full_values = sarima_full_idx.fittedvalues.tolist() + fc_mean_idx.tolist()
ax.plot(full_index, full_values, color='orange', linewidth=2, label='Fitted / Forecast')
ax.fill_between(fc_mean_idx.index, fc_ci_idx.iloc[:, 0], fc_ci_idx.iloc[:, 1], color='orange', alpha=0.2, label='95% CI')
ax.axvline(ts_full_idx.index[-1], color='gray', linestyle=':')
ax.set_title('12-Month Revenue Forecast (Index)', fontsize=13, fontweight='bold')
ax.set_ylabel('Revenue Index (2021 total = 100)')
ax.legend()
plt.tight_layout()
plt.savefig('chart_forecast_idx.png', dpi=150, bbox_inches='tight')
plt.close()
print('8/9 forecast done')

# ---------------------------------------------------------------------------
# 9. Model comparison chart -> index
test_idx = idx(mc['test'])
sarima_pred_idx = idx(mc['sarima_pred'])
prophet_pred_idx = idx(mc['prophet_pred'])
ts_full_for_plot = idx(mc['ts_full'])
train_idx = idx(mc['train'])

fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(ts_full_for_plot.index, ts_full_for_plot.values, 'o-', color='steelblue', label='Actual', linewidth=2)
ax.plot(test_idx.index, sarima_pred_idx.values, 's--', color='darkorange', label='SARIMA forecast')
ax.plot(test_idx.index, prophet_pred_idx.values, '^--', color='seagreen', label='Prophet forecast')
ax.axvline(train_idx.index[-1], color='gray', linestyle=':', label='Train/test split')
ax.set_title('Held-out Forecast Accuracy: SARIMA vs. Prophet (Index)', fontsize=13, fontweight='bold')
ax.set_ylabel('Revenue Index (2021 total = 100)')
ax.legend()
plt.tight_layout()
plt.savefig('chart_model_comparison_idx.png', dpi=150, bbox_inches='tight')
plt.close()
print('9/9 model_comparison done')

print('\\nAll indexed charts written.')
