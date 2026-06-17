# Customer / Sales Data Analysis — Summary Report

**Project:** Customer / Sales Data Analysis using Python
**Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn
**Dataset:** Synthetic retail sales transactions, Jan 2024 – Dec 2025 (3,000 orders, 1,017 unique customers)

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
| Total Revenue | Rs.49,043,936.07 |
| Total Orders | 3,000 |
| Unique Customers | 1,017 |
| Average Order Value | Rs.16,347.98 |
| Repeat Customers | 696 (68.4% of customers) |
| Best-Performing Month | 2024-11 (Rs.3,371,411.16) |

## 3. Revenue by Product Category

| Category | Revenue | Share of Total |
|---|---|---|
| Electronics | Rs.38,455,524.44 | 78.4% |
| Home & Kitchen | Rs.3,769,164.49 | 7.7% |
| Clothing | Rs.2,545,447.18 | 5.2% |
| Sports & Fitness | Rs.1,999,525.69 | 4.1% |
| Beauty & Personal Care | Rs.1,301,212.08 | 2.7% |
| Groceries | Rs.696,276.26 | 1.4% |
| Books | Rs.276,785.93 | 0.6% |

**Electronics** is the leading category by revenue, contributing
Rs.38,455,524.44 (78.4% of total sales) — disproportionate to
its share of order volume, since individual electronics transactions
carry a much higher average ticket size than categories like Books or
Groceries.

## 4. Revenue by Region

| Region | Revenue | Share of Total |
|---|---|---|
| North | Rs.14,622,988.39 | 29.8% |
| West | Rs.13,849,592.92 | 28.2% |
| South | Rs.13,435,947.62 | 27.4% |
| East | Rs.7,135,407.14 | 14.5% |

**North** leads regional revenue at Rs.14,622,988.39. The
gap between the top three regions (North, West, South) is relatively
narrow, while East lags meaningfully behind — a potential target for
expansion or localized marketing.

## 5. Payment Method Preferences

| Payment Method | Orders | Share |
|---|---|---|
| UPI | 1014 | 33.8% |
| Credit Card | 630 | 21.0% |
| Debit Card | 546 | 18.2% |
| Cash on Delivery | 472 | 15.7% |
| Net Banking | 338 | 11.3% |

Digital payment methods (UPI, Credit/Debit Card, Net Banking) account for
the large majority of transactions, with **UPI** the single most common
method — consistent with broader digital-payment adoption trends in the
Indian retail market.

## 6. Sales Trend

Monthly revenue shows a clear seasonal pattern: a sustained rise heading
into **2024-11**, the single best-performing month, driven by
festive-season demand (Diwali sales, year-end promotions). See
`visuals/01_monthly_sales_trend.png` for the full trend line.

## 7. Correlation Analysis

| Relationship | Correlation |
|---|---|
| Unit Price vs Total Sales | 0.82 |
| Quantity vs Total Sales | 0.28 |
| Discount % vs Customer Satisfaction | -0.07 |

- **Unit Price is the dominant driver of order value** (correlation =
  0.82), far outweighing quantity purchased
  (correlation = 0.28). This confirms that
  high-ticket categories like Electronics move total revenue more than
  multi-item basket size does.
- **Discounting shows a weak negative correlation with satisfaction**
  (-0.07), suggesting that, in this
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
