# -*- coding: utf-8 -*-
"""
Builds SAENAL_Report_v3.pdf. Naturalized-tone pass: fewer/less uniform callout
boxes, fewer em-dashes, more varied sentence rhythm, closer to how the author
writes elsewhere in this project (see notebook markdown cells).
"""
import weasyprint

CSS = """
<style>
@page {
    size: Letter;
    margin: 2.1cm 2cm 2.4cm 2cm;
    @bottom-center {
        content: "SAENAL Market — Sales Analysis & Forecast Report (v3)";
        font-size: 8pt;
        color: #888;
        font-family: 'Noto Sans CJK JP', sans-serif;
    }
    @bottom-right {
        content: counter(page);
        font-size: 8pt;
        color: #888;
    }
}
@page cover {
    margin: 0;
    @bottom-center { content: none; }
    @bottom-right { content: none; }
}
* { box-sizing: border-box; }
body {
    font-family: 'Noto Sans CJK JP', 'Helvetica Neue', Arial, sans-serif;
    font-size: 10.3pt;
    line-height: 1.5;
    color: #1a1a1a;
}
.cover {
    page: cover;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 3.2cm;
    background: linear-gradient(160deg, #0f3d5c 0%, #145374 55%, #1c6e8c 100%);
    color: white;
}
.cover .tag {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 3px;
    padding: 3px 10px;
    font-size: 9.5pt;
    letter-spacing: 0.06em;
    margin-bottom: 22px;
    width: fit-content;
}
.cover h1 { font-size: 30pt; margin: 0 0 6px 0; font-weight: 700; line-height: 1.25;}
.cover h2 { font-size: 14pt; font-weight: 400; margin: 0 0 40px 0; color: #cfe8f3; }
.cover .meta { font-size: 10.5pt; color: #e4f1f7; line-height: 1.9; }
.cover .meta b { color: white; }
.cover .footnote { position: absolute; bottom: 2cm; left: 3.2cm; font-size: 8.5pt; color: #bcd9e6; }

h1.section {
    font-size: 16pt;
    color: #0f3d5c;
    border-bottom: 2.5px solid #0f3d5c;
    padding-bottom: 5px;
    margin-top: 26px;
    margin-bottom: 12px;
    page-break-after: avoid;
}
h2.sub {
    font-size: 12.5pt;
    color: #145374;
    margin-top: 20px;
    margin-bottom: 8px;
    page-break-after: avoid;
}
h3.subsub {
    font-size: 11pt;
    color: #1c6e8c;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
}
p { margin: 6px 0 10px 0; text-align: justify; }
ul, ol { margin: 6px 0 12px 22px; padding: 0; }
li { margin-bottom: 4px; }
strong { color: #0f3d5c; }

table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 16px 0;
    font-size: 9.2pt;
}
th {
    background: #145374;
    color: white;
    text-align: left;
    padding: 6px 8px;
    font-weight: 600;
}
td {
    padding: 5px 8px;
    border-bottom: 1px solid #e0e0e0;
    vertical-align: top;
}
tr:nth-child(even) td { background: #f6fafc; }

.callout {
    border-left: 4px solid #1c6e8c;
    background: #eef6f9;
    padding: 8px 12px;
    margin: 10px 0 14px 0;
    font-size: 9.6pt;
}
.callout .label {
    font-weight: 700;
    color: #0f3d5c;
    text-transform: uppercase;
    font-size: 8pt;
    letter-spacing: 0.05em;
    display: block;
    margin-bottom: 3px;
}
.callout.warn { border-left-color: #b8590a; background: #fdf3ea; }
.callout.warn .label { color: #b8590a; }
.callout.fix { border-left-color: #2e8b57; background: #eaf6ef; }
.callout.fix .label { color: #1f6b41; }
.callout.risk { border-left-color: #b22222; background: #fbeaea; }
.callout.risk .label { color: #8f1c1c; }

figure { margin: 12px 0; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; border: 1px solid #ddd; border-radius: 3px; }
figcaption { font-size: 8.6pt; color: #666; margin-top: 4px; text-align: center; }

.badge {
    display: inline-block;
    background: #ffb703;
    color: #1a1a1a;
    font-size: 7.8pt;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 3px;
    margin-left: 6px;
    vertical-align: middle;
}
.small { font-size: 8.8pt; color: #555; }
</style>
"""

def callout(label, text, kind=""):
    return f'<div class="callout {kind}"><span class="label">{label}</span>{text}</div>'

def fig(src, caption):
    return f'<figure><img src="{src}"><figcaption>{caption}</figcaption></figure>'

HTML_PARTS = []

HTML_PARTS.append(f"""
<html><head><meta charset="utf-8">{CSS}</head><body>

<div class="cover">
  <div class="tag">INTERNSHIP PROJECT · UPDATED ANALYSIS</div>
  <h1>SAENAL Market</h1>
  <h2>Sales Analysis and Forecast Report — v3</h2>
  <div class="meta">
    <b>Prepared by:</b> Park Dongjae<br>
    <b>Data Coverage:</b> July 2021 – July 2024<br>
    <b>Methods:</b> EDA · SKU-Level RFM Segmentation · Category Portfolio Analysis (Growth-Share) ·
    SARIMA vs. Prophet Forecast Benchmarking · Vendor Concentration (HHI/CR4) · Correlation Analysis
  </div>
  <div class="footnote">This update adds four new analyses and fixes two data-quality issues found while
  building them. Figures are computed directly from the source Excel exports.</div>
</div>

<h1 class="section">1. Executive Summary</h1>
<p>This report covers SAENAL Market's sales performance from July 2021 through July 2024. The original
scope was annual and monthly revenue decomposition, category performance, loyalty-program segmentation, and
a SARIMA revenue forecast. This update adds four things on top of that: a SKU-level RFM segmentation of the
product catalog, a growth-share matrix for category profitability, a head-to-head SARIMA vs. Prophet
forecast comparison, and a proper quantified vendor concentration check using HHI and CR4 instead of a
listing-count chart.</p>

<p>Five things stand out from the data:</p>
<ul>
<li><strong>건강 is still the growth story, and it turns out it isn't alone.</strong> The category grew
+177% YoY and remains the clear leader. A data-quality fix in Section 4 also shows that 건강식품, which
looked like it was declining, is actually a stable second category of similar size.</li>
<li><strong>The loyalty program is a real multiplier.</strong> Member customers generate roughly 5–6x the
revenue of non-members in a comparable period.</li>
<li><strong>Vendor concentration looks worse once you measure it by revenue instead of listing count.</strong>
By listing count the platform looks fine (HHI 128). By revenue, the top vendor alone (아임굿) holds 21.8%
of platform revenue and 78% of the 건강식품 category, both above a reasonable exposure cap.</li>
<li><strong>The product portfolio is a textbook Pareto curve.</strong> About 12% of SKUs ("Star Performers")
generate 51% of revenue. A 196-SKU group I'm calling "Declining Stars" made up 23% of historical revenue
but has gone quiet recently and is worth a merchandising look.</li>
<li><strong>SARIMA actually does beat Prophet here, not just by assumption.</strong> A held-out accuracy
test puts SARIMA's MAPE at 23.9% against Prophet's 41.0%, which is enough of a gap to justify sticking with
SARIMA given the short history and strong seasonal pattern.</li>
</ul>

<table>
<tr><th style="width:20%">Finding</th><th>Analysis &amp; Implication</th></tr>
<tr><td><b>Peak Year</b></td><td>2022 revenue (sales-ledger basis) came in around ₩3.40B, the highest in the
dataset. 2023 dropped 10.6% to ₩3.04B. 2024's partial year (Jan–Jul) is at ₩2.15B, which annualizes to
roughly ₩3.5–3.7B.</td></tr>
<tr><td><b>Category Leaders</b></td><td>건강 and 건강식품 together account for about 62% of 2023
category-level revenue. Both are confirmed Stars in the growth-share matrix once a preprocessing bug that
had misclassified a large chunk of revenue as "Unknown" was fixed.</td></tr>
<tr><td><b>SKU Portfolio (RFM)</b></td><td>250 "Star Performer" SKUs (12% of
the catalog) generate 51.4% of revenue. 196 "Declining Stars" (9% of the catalog, 23.3% of historical
revenue) haven't sold in over two years.</td></tr>
<tr><td><b>Vendor Concentration</b></td><td>HHI on a revenue basis is 997 and
has been climbing since 2022 (633 → 1,928 by 2024). The top vendor, 아임굿, holds 21.8% of platform revenue
and 78.1% of the 건강식품 category.</td></tr>
<tr><td><b>Forecast Model Choice</b></td><td>SARIMA(1,1,1)(1,1,1,12) beats
Prophet on held-out MAE, RMSE, and MAPE (23.9% vs. 41.0%). SARIMA is used for the production forecast.</td></tr>
<tr><td><b>Loyalty Program ROI</b></td><td>Members generate roughly 5–6x non-member revenue per comparable
period, still the single highest-leverage lever in the dataset.</td></tr>
</table>
""")

HTML_PARTS.append("""
<h1 class="section">2. Introduction &amp; Objectives</h1>
<p>SAENAL Market operates in the increasingly competitive Korean online food and health marketplace. This
report turns three-plus years of transactional exports into things a small analytics team can actually act
on. The original version answered four questions. Four more came up naturally once those first findings
needed to turn into decisions:</p>
<ol>
<li>Where does revenue actually come from, in terms of categories, products, and customer segments?</li>
<li>How does seasonality shape demand, and is the business capitalizing on peak periods?</li>
<li>Is the loyalty program working as intended?</li>
<li>What does the revenue trajectory look like through 2025?</li>
<li> Which SKUs deserve inventory priority, and which ones are quietly taking
up shelf space for no return? (Section 6.3)</li>
<li> Which categories are actually profitable growth engines versus cash cows,
on a like-for-like yearly basis? (Section 6.2)</li>
<li> Is SARIMA the right forecasting model, or just the default one? (Section 10.2)</li>
<li> How concentrated is supplier risk, really, once you measure it properly?
(Section 9)</li>
</ol>
""")

HTML_PARTS.append("""
<h1 class="section">3. Data Overview &amp; Limitations</h1>
<p>The dataset spans July 2021 through July 2024 and comes from three source tables: a daily sales ledger
(order count, revenue, refunds, no customer identifier), a yearly product-performance snapshot (per-SKU
orders, revenue, refund rate, one file per year), and a product/category master list. There's no customer
ID anywhere in the export.</p>
""" +
callout("Data limitation", "Classic RFM analysis segments customers using per-customer purchase history. "
    "This dataset can't support that since there's no customer-level identifier at any grain. Section 6.3 "
    "adapts the same Recency/Frequency/Monetary logic to the SKU level instead, which the business can act "
    "on directly (inventory, delisting, reorder priority) and which the yearly product snapshots actually "
    "support.", "warn") +
"""
<table>
<tr><th>Table</th><th>Grain</th><th>Key fields</th><th>Used for</th></tr>
<tr><td>Daily sales ledger</td><td>1 row / day</td><td>order count, revenue, refunds</td>
<td>Revenue trend, seasonality, SARIMA/Prophet forecast (Sections 5, 10)</td></tr>
<tr><td>Yearly product snapshot</td><td>1 row / product / year</td><td>orders, revenue, refund rate,
avg. price</td><td>Category, vendor, RFM, correlation analysis (Sections 6, 7, 8, 9)</td></tr>
<tr><td>Product/category master</td><td>1 row / SKU</td><td>category ID, discount eligibility</td>
<td>Category and discount-segment labeling</td></tr>
</table>
<p class="small">The sales-ledger revenue total and the product-snapshot revenue total don't reconcile to
the same figure for a given year, since they come from different exports with different scope. This report
follows the same convention as the original: the sales ledger is used for revenue trend and forecasting
figures, and the product snapshot is used for category, vendor, and SKU-level shares. Shares within each
table are internally consistent even though the two totals differ.</p>
""")

HTML_PARTS.append("""
<h1 class="section">4. Data Preprocessing &amp; Quality Fixes</h1>
<p>Preprocessing already involved a few judgment calls documented previously: product-name standardization,
bracket-pattern company extraction (recovering most missing vendor fields), and removing three deprecated
category codes. Building the four new analyses surfaced two more issues that hadn't been caught before, so
both are fixed here, upstream of everything else in this report.</p>

<h3 class="subsub">4.1 Hidden whitespace in categorical labels</h3>
<p><code>Category</code>, <code>Company</code>, and <code>Discount Target</code> all carry a trailing
non-breaking space inherited from the Excel export. This didn't break the earlier <code>groupby()</code>
aggregations, since every row for a given label carried the same hidden character, but it silently breaks
any exact-match filter. It's stripped here before it can affect the vendor-matching logic in Section 9.</p>

<h3 class="subsub">4.2 A promotional SKU was counted as its own vendor</h3>
<p>The bracket-extraction regex pulled the entire promotional campaign text out of a milestone SKU name,
<code>[아임굿 1st 원데이 이벤트 100만포 돌파 감사 이벤트]</code>, and treated it as a separate vendor. That
one mislabeled bucket carried about ₩934M in revenue, enough to change who the #1 vendor is by revenue. It's
folded back into the real vendor, 아임굿, before the concentration analysis in Section 9.</p>

<h3 class="subsub">4.3 That fix also changed a category-level finding</h3>
<p>Fixing 4.2 had a knock-on effect worth calling out directly. The same mislabeled SKU had also failed to
match the product master list on <code>Category</code>, so its ~₩930M in revenue had landed in the catch-all
<code>Unknown</code> bucket instead of its real category. Once the vendor label was corrected, the
category-fill logic assigned it correctly to 건강식품, since that's what the rest of 아임굿's catalog is
categorized as.</p>
""" +
callout("Before / after", "'Unknown' category revenue for 2023 drops from about ₩965M to ₩31M. "
    "건강식품's 2023 revenue rises from ₩313M to ₩1.25B, which flips its year-over-year growth reading from "
    "−73.8% to +4.7%. That's the difference between a category that looks like it's dying and one that's "
    "actually stable. See Section 6.2 for the corrected matrix.", "fix") +
"""
<p class="small">Worth remembering for future data pulls: any regex-based field derivation should be spot
checked against the size of the "Unknown" bucket before trusting category-level comparisons. One mislabeled
high-revenue SKU moved a category's growth rate by more than 70 points.</p>
""")

HTML_PARTS.append("""
<h1 class="section">5. Revenue &amp; Seasonality Analysis</h1>
<h2 class="sub">5.1 Revenue Trends Over Time</h2>
""" +
fig("chart_revenue_trends.png", "Figure 1. Monthly sales trends by year (left) and annual totals (right), "
    "2021–2024.") +
"""
<table>
<tr><th>Year</th><th>Revenue (KRW)</th><th>Coverage</th><th>Annualized Estimate</th></tr>
<tr><td>2021</td><td>~₩710M</td><td>Jul–Dec (6 mo)</td><td>~₩1.42B</td></tr>
<tr><td>2022</td><td>~₩3.40B</td><td>Full Year</td><td>₩3.40B (actual peak)</td></tr>
<tr><td>2023</td><td>~₩3.04B</td><td>Full Year</td><td>₩3.04B (−10.6% YoY)</td></tr>
<tr><td>2024</td><td>~₩2.15B</td><td>Jan–Jul (7 mo, partial)</td><td>~₩3.5–3.7B annualized</td></tr>
</table>
<p>2022's peak is followed by a real but modest 2023 contraction, not a collapse. 2024's partial-year pace
points toward a recovery near or above the 2022 peak if the usual H2 seasonal pattern holds. Section 10
tests this directly.</p>

<h2 class="sub">5.2 Monthly Seasonality</h2>
""" +
fig("chart_avg_monthly.png", "Figure 2. Average monthly revenue across all years. December, June, and "
    "November are consistent peaks; July is the structural trough.") +
"""
<p>December (~₩300M average), June, and November are consistent peaks across multiple years, which points
to structural demand cycles rather than one-off promotions. July and August sit about 50% below peak
months, a predictable, calendar-certain gap that's still underused as a planning input (see
Recommendations).</p>
""")

HTML_PARTS.append("""
<h1 class="section">6. Category &amp; Product Portfolio Analysis</h1>
<h2 class="sub">6.1 Category Revenue Decomposition</h2>
""" +
fig("chart_category_revenue.png", "Figure 3. Revenue by year and category. 건강 and 건강식품's rise "
    "dominates the mix; about 30 other categories compete for the remainder.") +
fig("chart_category_top10.png", "Figure 4. Category frequency (product count, left) and top-10 products by "
    "total revenue (right).") +
"""
<h2 class="sub">6.2 Category Profitability Matrix (Growth–Share)</h2>
<p>SAENAL Market doesn't capture COGS or margin at the product level, so a true profitability matrix isn't
possible here. As a proxy, this builds a BCG-style growth-share matrix instead: YoY revenue growth
(2022→2023, the two full calendar years available) plotted against revenue share of the platform, with
bubble size showing order volume. 'Unknown' is excluded as a data artifact rather than a real category.</p>
""" +
fig("chart_category_matrix.png", "Figure 5. Category portfolio matrix, growth vs. share, after the "
    "data-quality fix in Section 4.3.") +
"""
<table>
<tr><th>Category</th><th>2023 Revenue</th><th>YoY Growth</th><th>Share</th><th>Quadrant</th></tr>
<tr><td>건강</td><td>₩1,262M</td><td>+177.0%</td><td>31.0%</td><td>Star</td></tr>
<tr><td>건강식품</td><td>₩1,247M</td><td>+4.7%</td><td>30.7%</td><td>Star</td></tr>
<tr><td>국/탕/찌개/면</td><td>₩278M</td><td>−44.2%</td><td>6.8%</td><td>Cash Cow</td></tr>
<tr><td>뷰티/다이어트</td><td>₩236M</td><td>+58.8%</td><td>5.8%</td><td>Star</td></tr>
<tr><td>수산/건어물/김</td><td>₩165M</td><td>−27.1%</td><td>4.0%</td><td>Cash Cow</td></tr>
<tr><td>밥/반찬/요리</td><td>₩155M</td><td>−53.2%</td><td>3.8%</td><td>Cash Cow</td></tr>
<tr><td>식품</td><td>₩75M</td><td>+74.8%</td><td>1.9%</td><td>Question Mark</td></tr>
</table>
<p><b>Reading it:</b> 건강 and 건강식품 together make up 61.7% of category-level revenue and both are
Stars. That's good news in the sense that demand is still growing and not yet saturated, but it also means
the vendor concentration in Section 9 and this category concentration compound each other. A few staple
categories (국/탕/찌개/면, 밥/반찬/요리, 수산/건어물/김) are Cash Cows: stable volume, negative growth,
still worth defending but not where new investment should go.</p>

<h2 class="sub">6.3 SKU-Level RFM Segmentation</h2>
<p>Adapted to the SKU level since there's no customer ID (Section 3): Recency is years since a product last
sold, Frequency is total order count, Monetary is total revenue. Each is scored 1–5 and combined into six
portfolio segments.</p>
""" +
fig("chart_rfm_segments.png", "Figure 6. SKU count (left) and revenue share (right) by RFM segment.") +
"""
<table>
<tr><th>Segment</th><th>SKUs</th><th>Revenue Share</th><th>Interpretation</th></tr>
<tr><td><b>Star Performers</b></td><td>250 (12%)</td><td>51.4%</td><td>Core catalog. Protect availability
and pricing.</td></tr>
<tr><td><b>Declining Stars (At Risk)</b></td><td>196 (9%)</td><td>23.3%</td><td>Historically high revenue,
no recent sales. Likely delisted, out of stock, or losing placement.</td></tr>
<tr><td><b>Steady Sellers</b></td><td>650 (31%)</td><td>22.2%</td><td>Reliable mid-tier catalog depth.</td></tr>
<tr><td><b>Needs Review</b></td><td>589 (28%)</td><td>2.6%</td><td>Mixed signals, not urgent.</td></tr>
<tr><td><b>Dormant / Long-tail</b></td><td>346 (16%)</td><td>0.5%</td><td>Low on everything. Candidates for
delisting.</td></tr>
<tr><td><b>New / Niche SKUs</b></td><td>86 (4%)</td><td>0.1%</td><td>Recently active, low volume, too early
to judge.</td></tr>
</table>
<p>The Declining Stars segment is probably the most useful output of this whole exercise: 196 SKUs that
used to generate real revenue, 23.3% of the portfolio's historical total, have gone quiet. Before assuming
demand just disappeared, it's worth checking whether these are simply out of stock or lost search placement.
Reactivating even a third of this segment would likely move the needle more than most new product
launches.</p>
""")

HTML_PARTS.append("""
<h1 class="section">7. Customer Behavior &amp; Loyalty Program</h1>
""" +
fig("chart_discount_revenue.png", "Figure 7. Total revenue by discount/membership segment. 회원 (Member) "
    "dominates.") +
"""
<table>
<tr><th>Segment</th><th>Revenue</th><th>Interpretation</th></tr>
<tr><td>회원 (Member)</td><td>~₩7.5–8B</td><td>The clear revenue engine: higher frequency, larger basket
size, lower price sensitivity.</td></tr>
<tr><td>할인불가 (Non-Member)</td><td>~₩2.8B</td><td>Distant second. The conversion opportunity.</td></tr>
<tr><td>Unknown</td><td>~₩1B</td><td>Lost segmentation intelligence. Membership should be captured at
checkout.</td></tr>
</table>
<p>Members generate roughly 5–6x the revenue of non-members per comparable period. That gap is too large to
be explained by discount-seeking alone, since typical discount uplift runs 10–20%, not 500%+. It looks more
like the loyalty program changes purchasing behavior structurally rather than just subsidizing demand that
would have happened anyway. Converting 15% of non-member purchasers to membership-equivalent behavior would
be worth an estimated ₩280–420M.</p>
""")

HTML_PARTS.append("""
<h1 class="section">8. Correlation Analysis</h1>
""" +
fig("chart_correlation.png", "Figure 8. Correlation heatmap (Pearson r) across key numeric variables.") +
"""
<table>
<tr><th>Variable Pair</th><th>r</th><th>Interpretation</th></tr>
<tr><td>Num. Order → Revenue</td><td>0.46</td><td>Moderate. Volume matters, but product mix and pricing
tier explain more of the variance.</td></tr>
<tr><td>Refund Rate → Revenue</td><td>−0.01</td><td>Effectively zero. Refund-prone products aren't
punished by customers in any systematic way.</td></tr>
<tr><td>Avg. Price → Revenue</td><td>0.23</td><td>Weak. Pricing strategy isn't the primary lever here;
multiple willingness-to-pay tiers coexist.</td></tr>
</table>
""" +
fig("chart_pairplot.png", "Figure 9. Pairplot across key variables, top-5 categories.") +
"""
""")

HTML_PARTS.append("""
<h1 class="section">9. Vendor Concentration — Quantified</h1>
<p>The original report flagged vendor risk using a listing-frequency chart: 대도 had far more rows than
anyone else across the four yearly snapshots. That metric mixes up a vendor's tenure (how many years it's
been listed) with its actual economic weight (how much revenue depends on it). A vendor listed every year
racks up rows regardless of how much it actually sells. This section replaces that read with the
Herfindahl–Hirschman Index (HHI) and top-4 concentration ratio (CR4), computed on four different bases.</p>
""" +
fig("chart_vendor_concentration.png", "Figure 10. HHI across four concentration bases (left) and the top "
    "revenue vendor's exposure by category (right).") +
"""
<table>
<tr><th>Basis</th><th>Top Vendor</th><th>Top Share</th><th>HHI</th><th>CR4</th><th>Read</th></tr>
<tr><td>Listing frequency (v2 metric)</td><td>대도</td><td>8.3%</td><td>128</td><td>16.1%</td>
<td>Looks competitive, but measures tenure, not weight.</td></tr>
<tr><td>Unique SKU count</td><td>경영푸드</td><td>3.2%</td><td>56</td><td>10.8%</td><td>Even more diffuse.
No single vendor dominates by SKU count.</td></tr>
<tr><td>Order volume</td><td>밥도둑푸드</td><td>15.1%</td><td>368</td><td>30.3%</td><td>More concentrated
than SKU count would suggest.</td></tr>
<tr><td><b>Revenue (economic weight)</b></td><td><b>아임굿</b></td><td><b>21.8%</b></td><td><b>997</b></td>
<td><b>53.8%</b></td><td><b>The metric that actually matters for supply risk.</b></td></tr>
</table>
<p>아임굿 is the platform's largest vendor by revenue at 21.8% of the total, above a 20% single-vendor
exposure guideline, and it holds 78.1% of the entire 건강식품 category's revenue. If 아임굿 exits,
renegotiates unfavorably, or runs into a supply disruption, close to 30% of platform revenue is directly
exposed through one vendor relationship. That's a meaningfully different risk picture than the original
listing-count chart implied.</p>

<h2 class="sub">9.1 Concentration Trend</h2>
<table>
<tr><th>Year</th><th>HHI (revenue basis)</th><th>CR4</th><th>Active Vendors</th></tr>
<tr><td>2021</td><td>1,338</td><td>65.6%</td><td>117</td></tr>
<tr><td>2022</td><td>633</td><td>38.2%</td><td>609</td></tr>
<tr><td>2023</td><td>1,506</td><td>61.9%</td><td>578</td></tr>
<tr><td>2024 (partial)</td><td>1,928</td><td>69.8%</td><td>242</td></tr>
</table>
<p>Concentration eased in 2022 as the vendor base expanded from 117 to 609 active vendors, then climbed back
through 2023–2024 even though the vendor count held roughly steady. Revenue is consolidating onto fewer,
larger suppliers rather than the catalog genuinely diversifying. This is worth checking quarterly rather
than treating as a one-time finding.</p>
""")

HTML_PARTS.append("""
<h1 class="section">10. Revenue Forecasting</h1>
<h2 class="sub">10.1 Seasonal Decomposition</h2>
""" +
fig("chart_decomposition.png", "Figure 11. Seasonal decomposition of monthly revenue: trend plus yearly "
    "seasonal component.") +
"""
<h2 class="sub">10.2 Model Comparison: SARIMA vs. Prophet</h2>
<p>Before settling on a single forecasting approach, SARIMA is benchmarked against Facebook Prophet on a
proper held-out test. The last 6 full months are excluded from training, both models forecast that window,
and accuracy is scored on MAE, RMSE, and MAPE. The most recent month (2024-07) is excluded from both train
and test because the underlying export was pulled mid-month, so it's a partial month rather than a genuine
data point.</p>
""" +
fig("chart_model_comparison.png", "Figure 12. Held-out forecast accuracy: SARIMA vs. Prophet, last 6 "
    "months.") +
"""
<table>
<tr><th>Model</th><th>MAE</th><th>RMSE</th><th>MAPE</th></tr>
<tr><td><b>SARIMA(1,1,1)(1,1,1,12)</b></td><td>₩60.5M</td><td>₩94.9M</td><td><b>23.9%</b></td></tr>
<tr><td>Prophet</td><td>₩140.3M</td><td>₩168.0M</td><td>41.0%</td></tr>
</table>
<p>SARIMA wins on all three metrics. With only about 2.5 years of training history and a strong, regular
12-month cycle, its explicit seasonal order captures the pattern more reliably than Prophet's
changepoint-based trend model, which tends to need more history before its flexibility pays off. This
confirms, rather than just assumes, that SARIMA is the right production model given how much data is
available and how regular the seasonality is.</p>

<h2 class="sub">10.3 Final Forecast (SARIMA)</h2>
""" +
fig("chart_sarima_fit.png", "Figure 13. SARIMA fit validation: observed vs. fitted, full history.") +
fig("chart_forecast.png", "Figure 14. 12-month forward forecast with 95% confidence interval, refit on the "
    "complete history.") +
"""
<p>Monthly peaks in late 2025 are projected in the ₩420–500M range, roughly 25–40% above 2024's observed
peaks, driven by trend accumulation plus seasonal uplift. The confidence interval widens noticeably past
Q3 2025, so quarterly recalibration is still the right approach for planning purposes.</p>
""")

HTML_PARTS.append("""
<h1 class="section">11. Key Findings Summary</h1>
<table>
<tr><th>Finding</th><th>Quantified Insight</th></tr>
<tr><td>Revenue Trajectory</td><td>2022 peak, 2023 contraction (−10.6%), 2024 recovery pace of roughly
₩3.5–3.7B annualized.</td></tr>
<tr><td>Seasonality</td><td>About a 2x revenue gap between the December peak and July trough. Structural
and calendar-predictable.</td></tr>
<tr><td>Category Concentration</td><td>건강 + 건강식품 make up 61.7% of category revenue, both confirmed
Stars after the data fix. No saturation signal in either.</td></tr>
<tr><td>SKU Portfolio</td><td>12% of SKUs generate 51% of revenue. A 196-SKU
"Declining Stars" segment (23% of historical revenue) needs a stock/placement check.</td></tr>
<tr><td>Vendor Concentration</td><td>Revenue-basis HHI of 997, rising since
2022. The top vendor exceeds a 20% exposure guideline platform-wide and holds 78% of one category.</td></tr>
<tr><td>Forecast Model</td><td>SARIMA MAPE of 23.9% vs. Prophet's 41.0% on
held-out data. SARIMA confirmed as the better production model.</td></tr>
<tr><td>Loyalty Program ROI</td><td>Member segment generates roughly 5–6x non-member revenue. A 15%
conversion rate would be worth an estimated ₩280–420M.</td></tr>
<tr><td>Price Independence</td><td>r=0.23 price-revenue correlation. Brand trust and perceived value drive
purchasing more than price does.</td></tr>
</table>
""")

HTML_PARTS.append("""
<h1 class="section">12. Recommendations</h1>
<p>Ordered by estimated impact times feasibility. Items 1 through 3 and 6 carry over from the original
version and are still valid. 4, 5, and 7 are new and come directly out of this update's analyses.</p>
<h3 class="subsub">① Accelerate Loyalty Enrollment — Highest Priority</h3>
<p>Target converting 15%+ of non-member purchasers to membership within 12 months, using a 30-day free
trial, a real-time savings calculator at checkout, and a referral program.</p>
<h3 class="subsub">② Double Down on 건강 / 건강식품 — High Priority</h3>
<p>Both categories are confirmed Stars with no saturation signal. Onboard 3–5 new health-supplement brands
per quarter and develop cross-category bundles.</p>
<h3 class="subsub">③ Formalize a Seasonal Campaign Calendar — High Priority</h3>
<p>Pre-allocate budget to June, November, and December. Run summer-specific counter-programming, cooling
foods and electrolyte-type SKUs, for the July–August trough.</p>
<h3 class="subsub">④ Audit and Reactivate the "Declining Stars" SKU Segment — High Priority</h3>
<p>196 SKUs holding 23.3% of the portfolio's historical revenue have gone quiet over the last two-plus
years. Before writing this off as normal churn, check stock levels, search placement, and pricing for this
specific list. It's a bounded, prioritized task rather than a vague "reduce the long tail" initiative.</p>
<h3 class="subsub">⑤ Cap Single-Vendor Exposure, Starting with 아임굿 — High Priority</h3>
<p>아임굿 holds 78% of 건강식품 category revenue and 21.8% of platform revenue, both above a recommended
20% cap. Start qualifying a second supplier for 건강식품's top SKUs before this becomes a single point of
failure, especially since the category is one of the two Stars carrying platform growth.</p>
<h3 class="subsub">⑥ Standardize Data Infrastructure — Medium Priority (High Compound Value)</h3>
<p>Mandate membership capture at checkout and standardized product naming at vendor onboarding. Section 4
of this report shows a single bracket-extraction bug moved about ₩930M in revenue into the wrong category.
An automated check that flags when the "Unknown" bucket exceeds a threshold share of any metric would catch
this kind of thing earlier.</p>
<h3 class="subsub">⑦ Recalibrate the Forecast Quarterly Using SARIMA — Medium Priority</h3>
<p>Section 10 confirms SARIMA over Prophet given this dataset's length and seasonality. As more 2024–2025
data comes in, the same held-out benchmark should be re-run each quarter, since Prophet's disadvantage may
narrow with more training history and the model choice shouldn't be treated as permanent.</p>
""")

HTML_PARTS.append("""
<h1 class="section">13. Conclusion</h1>
<p>SAENAL Market's sales data tells a fairly coherent story: two structurally strong health categories, a
loyalty program that clearly changes customer behavior, and a predictable seasonal demand cycle that's
still underused as a planning input. This update sharpens that picture in two ways. First, both the product
portfolio and the vendor base turn out to be more concentrated than the original qualitative charts
suggested, a Pareto curve where 12% of SKUs drive 51% of revenue, and a top vendor that exceeds its own
recommended exposure cap. Second, it shows that a single upstream data-quality bug can flip a category's
growth story from declining to stable, which is a good reminder to sanity-check the "Unknown" bucket before
presenting category-level comparisons as findings.</p>
<p>Accelerating loyalty program enrollment is still the single most impactful action available. But the two
new findings from this update, the Declining Stars SKU segment and the 아임굿 vendor exposure, are the most
immediately actionable additions, since both come with a specific, bounded list to act on rather than a
general directional recommendation.</p>
""")

FULL_HTML = ''.join(HTML_PARTS) + "</body></html>"

with open('SAENAL_Report_v3.html', 'w', encoding='utf-8') as f:
    f.write(FULL_HTML)

weasyprint.HTML(string=FULL_HTML, base_url='.').write_pdf('SAENAL_Report_v3.pdf')
print('Wrote SAENAL_Report_v3.pdf,', len(FULL_HTML), 'chars of HTML')
