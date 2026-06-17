# Customer / Sales Data Analysis using Python

**Key Skills:** Python, Pandas, NumPy, Matplotlib, Seaborn, Statistics

A complete, reproducible data analysis project on a retail sales dataset.
It covers data generation/loading, cleaning, descriptive statistics,
trend analysis, correlation analysis, and visualization — packaged as
both a standalone script and an annotated Jupyter notebook.

## Project Structure

```
customer_sales_analysis/
├── data/
│   └── sales_data.csv              # 3,000-row synthetic retail transactions dataset
├── notebooks/
│   └── Customer_Sales_Analysis.ipynb  # Narrative walkthrough with inline charts
├── visuals/                        # All exported charts (PNG)
│   ├── 01_monthly_sales_trend.png
│   ├── 02_revenue_by_category.png
│   ├── 03_revenue_by_region.png
│   ├── 04_order_value_distribution.png
│   ├── 05_customer_age_distribution.png
│   ├── 06_correlation_heatmap.png
│   └── 07_payment_method_share.png
├── generate_data.py                # Creates the synthetic dataset
├── analysis.py                     # Full analysis pipeline (script form)
├── generate_report.py              # Builds summary_report.md from stats.json
├── descriptive_stats.csv           # Descriptive statistics output
├── correlation_matrix.csv          # Correlation matrix output
├── stats.json                      # All key computed metrics (machine-readable)
├── summary_report.md               # Human-readable findings report
└── README.md
```

## Dataset

A synthetic but realistic e-commerce/retail dataset (3,000 transactions,
Jan 2024 – Dec 2025) with:
- **Order info:** OrderID, OrderDate, Quantity, UnitPrice, DiscountPercent, TotalSales, PaymentMethod
- **Customer info:** CustomerID, Age, Gender, Region, City
- **Product info:** ProductCategory, Product
- **Feedback:** CustomerSatisfaction (1–5, with ~2% missing values for cleaning practice)

It includes deliberate real-world patterns: festive-season seasonality
(Oct–Dec revenue boost), a loyal-customer segment that orders
repeatedly, and category-driven price variation — so the analysis has
genuine signal to uncover, not just noise.

## How to Reproduce

```bash
pip install pandas numpy matplotlib seaborn

# 1. Generate the dataset
python generate_data.py

# 2. Run the full analysis (saves charts to visuals/, stats to stats.json)
python analysis.py

# 3. Build the Markdown summary report from the computed stats
python generate_report.py
```

Or open `notebooks/Customer_Sales_Analysis.ipynb` directly — it already
contains the executed outputs and charts, with narrative explanations
between each step.

## Analysis Highlights

- **Descriptive statistics** on order value, quantity, pricing, discounting, and satisfaction
- **Trend analysis**: monthly revenue trend, revenue by category/region
- **Distribution analysis**: histograms for order value and customer age
- **Correlation analysis**: heatmap across all numeric features, with written interpretation
- Findings are written up in `summary_report.md` with all figures pulled
  directly from the computed output (no hand-typed numbers)

## Key Findings (see `summary_report.md` for full detail)

- Electronics drives the large majority of revenue despite a mid-tier
  share of order volume — average ticket size matters more than basket size.
- Revenue peaks sharply in the Oct–Dec festive season.
- North and West are the strongest regions; East is comparatively under-penetrated.
- UPI is the most common payment method.
- Discount depth shows no meaningful positive correlation with customer satisfaction.

---
*Note: this dataset is synthetically generated for demonstration purposes.
Swap in your own sales data by replacing `data/sales_data.csv` with the
same column structure — the rest of the pipeline runs unchanged.*
