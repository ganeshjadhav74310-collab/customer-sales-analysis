"""
generate_report.py
-------------------
Builds summary_report.md from stats.json so every number in the report
is pulled directly from the actual analysis output (no hand-typed figures).
"""
import json

with open("stats.json") as f:
    s = json.load(f)

def inr(x):
    return f"Rs.{x:,.2f}"

cat_lines = "\n".join(
    f"| {cat} | {inr(rev)} | {rev / s['total_revenue'] * 100:.1f}% |"
    for cat, rev in s["category_sales"].items()
)
region_lines = "\n".join(
    f"| {reg} | {inr(rev)} | {rev / s['total_revenue'] * 100:.1f}% |"
    for reg, rev in s["region_sales"].items()
)
payment_lines = "\n".join(
    f"| {method} | {count} | {count / s['total_orders'] * 100:.1f}% |"
    for method, count in s["payment_counts"].items()
)

report = f"""# Customer / Sales Data Analysis — Summary Report

**Project:** Customer / Sales Data Analysis using Python
**Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn
**Dataset:** Synthetic retail sales transactions, Jan 2024 – Dec 2025 ({s['total_orders']:,} orders, {s['unique_customers']:,} unique customers)

---

## 1. Overview

This project analyzes a retail sales dataset to identify revenue trends,
customer purchasing patterns, and relationships between order
characteristics (price, quantity, discounting) and outcomes (total
sales, customer satisfaction). The workflow covers data loading and
cleaning, descriptive statistics, groupby-based trend analysis,
correlation analysis, and visualization.

## 2. Headline Metrics

| Metric | Value |
|---|---|
| Total Revenue | {inr(s['total_revenue'])} |
| Total Orders | {s['total_orders']:,} |
| Unique Customers | {s['unique_customers']:,} |
| Average Order Value | {inr(s['avg_order_value'])} |
| Repeat Customers | {s['repeat_customers']:,} ({s['repeat_rate_pct']:.1f}% of customers) |
| Best-Performing Month | {s['best_month']} ({inr(s['best_month_revenue'])}) |

## 3. Revenue by Product Category

| Category | Revenue | Share of Total |
|---|---|---|
{cat_lines}

**{s['top_category']}** is the leading category by revenue, contributing
{inr(s['top_category_revenue'])} ({s['top_category_revenue']/s['total_revenue']*100:.1f}% of total sales) — disproportionate to
its share of order volume, since individual electronics transactions
carry a much higher average ticket size than categories like Books or
Groceries.

## 4. Revenue by Region

| Region | Revenue | Share of Total |
|---|---|---|
{region_lines}

**{s['top_region']}** leads regional revenue at {inr(s['top_region_revenue'])}. The
gap between the top three regions (North, West, South) is relatively
narrow, while East lags meaningfully behind — a potential target for
expansion or localized marketing.

## 5. Payment Method Preferences

| Payment Method | Orders | Share |
|---|---|---|
{payment_lines}

Digital payment methods (UPI, Credit/Debit Card, Net Banking) account for
the large majority of transactions, with **UPI** the single most common
method — consistent with broader digital-payment adoption trends in the
Indian retail market.

## 6. Sales Trend

Monthly revenue shows a clear seasonal pattern: a sustained rise heading
into **{s['best_month']}**, the single best-performing month, driven by
festive-season demand (Diwali sales, year-end promotions). See
`visuals/01_monthly_sales_trend.png` for the full trend line.

## 7. Correlation Analysis

| Relationship | Correlation |
|---|---|
| Unit Price vs Total Sales | {s['corr_unitprice_totalsales']:.2f} |
| Quantity vs Total Sales | {s['corr_quantity_totalsales']:.2f} |
| Discount % vs Customer Satisfaction | {s['corr_discount_satisfaction']:.2f} |

- **Unit Price is the dominant driver of order value** (correlation =
  {s['corr_unitprice_totalsales']:.2f}), far outweighing quantity purchased
  (correlation = {s['corr_quantity_totalsales']:.2f}). This confirms that
  high-ticket categories like Electronics move total revenue more than
  multi-item basket size does.
- **Discounting shows a weak negative correlation with satisfaction**
  ({s['corr_discount_satisfaction']:.2f}), suggesting that, in this
  dataset, heavier discounting does not translate into higher customer
  satisfaction — promotions should be evaluated primarily on their
  revenue/margin impact rather than assumed goodwill benefits.

See `visuals/06_correlation_heatmap.png` for the full correlation matrix
across all numeric features.

## 8. Key Takeaways

1. Revenue is concentrated in a small number of high-value Electronics
   transactions rather than spread evenly across categories or driven by
   bulk purchasing.
2. The Oct–Dec festive window is the clearest, most repeatable revenue
   opportunity in the calendar and should anchor inventory and
   promotional planning.
3. North and West regions are the strongest markets; East represents
   the largest untapped growth opportunity.
4. UPI's dominance as a payment method reflects the shift toward
   instant digital payments and should be prioritized in checkout UX.
5. Discount depth alone is not a reliable lever for improving customer
   satisfaction in this dataset — other factors (product quality,
   delivery experience, etc.) likely matter more.

## 9. Files in This Project

- `data/sales_data.csv` — source dataset
- `generate_data.py` — synthetic data generation script
- `analysis.py` — full analysis pipeline (stats, correlation, charts)
- `notebooks/Customer_Sales_Analysis.ipynb` — notebook version with narrative + outputs
- `visuals/` — all generated charts (PNG)
- `descriptive_stats.csv`, `correlation_matrix.csv`, `stats.json` — raw numeric outputs
- `summary_report.md` — this report
"""

with open("summary_report.md", "w") as f:
    f.write(report)

print("summary_report.md written.")
