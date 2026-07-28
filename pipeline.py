import re
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')

YEARS = [2021, 2022, 2023, 2024]

def load_yearly(prefix: str) -> pd.DataFrame:
    frames = []
    for yr in YEARS:
        df = pd.read_excel(f'Saenal_market_{yr}_{prefix}.xlsx', engine='openpyxl')
        df['year'] = yr
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

products_raw  = load_yearly('product')
sales_raw     = load_yearly('sale')

category_id   = pd.read_excel('Saenal_market_categoryID.xlsx',    engine='openpyxl')
products_list = pd.read_excel('Saenal_market_products_list.xlsx', engine='openpyxl')

print('products_raw', products_raw.shape)
print('sales_raw', sales_raw.shape)

PRODUCT_COLS = {
    '상품명'        : 'Product',
    'year'          : 'Year',
    '평균 상품금액' : 'Avg. Price',
    '주문건수'      : 'Num. Order',
    '취소·반품 개수': 'Num. Refund',
    '취소·반품률'   : 'Refund Rate',
    '결제금액'      : 'Purchase $',
    '환불금액'      : 'Refund $',
    '매출금액'      : 'Revenues',
}

products = (
    products_raw
    .rename(columns=PRODUCT_COLS)
    [list(PRODUCT_COLS.values())]
    .assign(**{
        'Refund Rate': lambda df:
            pd.to_numeric(
                df['Refund Rate'].astype(str).str.replace('%', '', regex=False),
                errors='coerce'
            )
    })
    .query('`Refund Rate` <= 100')
    .reset_index(drop=True)
)
print('products', products.shape)

category_id = (
    category_id
    .rename(columns={'Category': '카테고리', 'Product Code': '카테고리 ID'})
    .dropna()
)
products_list = products_list.rename(columns={'카테고리ID': '카테고리 ID'})

DEPRECATED = {'CATE88', 'CATE40', 'CATE0'}
selling_products = products_list[
    ~products_list['카테고리 ID'].isin(DEPRECATED)
].copy()

selling_products = selling_products[
    ['상품명', '자체 상품코드', '카테고리 ID', '판매가', '세금', '할인적용대상', '할인금액']
]
selling_products['할인금액']     = selling_products['할인금액'].fillna(0)
selling_products['할인적용대상'] = selling_products['할인적용대상'].fillna('할인불가')

selling_prod_cate = selling_products.merge(category_id, on='카테고리 ID', how='left')
print('Active categories:', selling_prod_cate['카테고리 ID'].nunique())

def extract_company(name: str):
    m = re.search(r'\[(.+?)\]', str(name))
    return m.group(1).strip() if m else np.nan

products['Company']          = products['Product'].apply(extract_company)
selling_prod_cate['Company'] = selling_prod_cate['상품명'].apply(extract_company)

df = products.merge(
    selling_prod_cate[['상품명', '카테고리', '할인적용대상']].rename(columns={'상품명': 'Product'}),
    on='Product', how='left'
).rename(columns={'카테고리': 'Category', '할인적용대상': 'Discount Target'})
print('df after merge', df.shape)
print(df.isnull().sum())

df.loc[df['Product'].str.contains('셀핀다',         na=False), 'Company'] = '셀핀다'
df.loc[df['Product'].str.contains('하동 녹차 명란김', na=False), 'Company'] = '자연향기'

# v3 fix: the bracket-extraction regex pulled the full promo-campaign text out
# of a milestone SKU name (e.g. "[아임굿 1st 원데이 이벤트 100만포 돌파 감사 이벤트]")
# as if it were a distinct vendor. This single mislabeled bucket is large enough
# (~₩930M) to distort vendor concentration figures, so it is folded back into
# the real vendor before any concentration/HHI analysis.
df.loc[df['Company'].astype(str).str.startswith('아임굿'), 'Company'] = '아임굿'

df = df[~df['Product'].str.contains('개인결제창', na=False)].copy()

for col in ['Category', 'Discount Target']:
    df[col] = df.groupby('Company')[col].transform(
        lambda s: s.fillna(s.mode().iloc[0]) if not s.mode().empty else s
    )

df[['Company', 'Category', 'Discount Target']] = (
    df[['Company', 'Category', 'Discount Target']].fillna('Unknown')
)

# v3 fix: category/company/discount labels carry hidden non-breaking-space (\xa0)
# characters from the source Excel export. Left uncleaned, this silently
# fragments any groupby('Category') into duplicate-looking buckets and was not
# caught in the v2 analysis. Normalize whitespace before it feeds downstream
# aggregation (RFM, category matrix, vendor concentration).
for col in ['Company', 'Category', 'Discount Target']:
    df[col] = (
        df[col].astype(str)
        .str.replace('\xa0', ' ', regex=False)
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
    )

print('Final df shape:', df.shape)
print(df.isnull().sum())

sales = (
    sales_raw
    .assign(date  = lambda d: pd.to_datetime(d['일자']))
    .assign(year  = lambda d: d['date'].dt.year,
            month = lambda d: d['date'].dt.month)
)

monthly_pivot = (
    sales.groupby(['year', 'month'])['매출']
    .sum()
    .unstack(level='year')
)

monthly_ts = (
    sales.resample('ME', on='date')['매출']
    .sum()
    .rename('total_revenue')
    .reset_index()
    .rename(columns={'date': 'date'})
)

yearly_ts = sales.groupby('year')['매출'].sum()
print('\nYearly revenue (KRW):')
print(yearly_ts)

print('\nmonthly_ts tail:')
print(monthly_ts.tail())
print('\nmonthly_ts shape:', monthly_ts.shape)

# Save intermediates
df.to_pickle('df_products.pkl')
monthly_ts.to_pickle('monthly_ts.pkl')
products_raw.to_pickle('products_raw.pkl')
print('\nSaved df_products.pkl, monthly_ts.pkl, products_raw.pkl')
