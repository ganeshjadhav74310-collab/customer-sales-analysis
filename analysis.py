"""
analysis.py
-----------
Customer / Sales Data Analysis using Python
Key Skills demonstrated: Python, Pandas, NumPy, Matplotlib/Seaborn, Statistics

Pipeline:
1. Load & inspect the dataset
2. Clean data (handle missing values)
3. Descriptive statistics
4. Sales trend analysis (monthly / category / region)
5. Correlation analysis (heatmap)
6. Save all charts to visuals/ and key metrics to stats.json
7. Auto-generate a Markdown summary report (summary_report.md)
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 110

# ----------------------------------------------------------------------
# 1. LOAD & INSPECT
# ----------------------------------------------------------------------
df = pd.read_csv("data/sales_data.csv", parse_dates=["OrderDate"])

print("Shape:", df.shape)
print("\nDtypes:\n", df.dtypes)
print("\nMissing values:\n", df.isna().sum())

# ----------------------------------------------------------------------
# 2. CLEAN DATA
# ----------------------------------------------------------------------
# CustomerSatisfaction has a small % of missing values -> impute with median
df["CustomerSatisfaction"] = df["CustomerSatisfaction"].fillna(
    df["CustomerSatisfaction"].median()
)
df["OrderMonth"] = df["OrderDate"].dt.to_period("M").astype(str)
df["OrderQuarter"] = df["OrderDate"].dt.to_period("Q").astype(str)

# ----------------------------------------------------------------------
# 3. DESCRIPTIVE STATISTICS
# ----------------------------------------------------------------------
numeric_cols = ["Age", "Quantity", "UnitPrice", "DiscountPercent", "TotalSales", "CustomerSatisfaction"]
desc_stats = df[numeric_cols].describe().round(2)
print("\nDescriptive statistics:\n", desc_stats)

total_revenue = df["TotalSales"].sum()
total_orders = len(df)
unique_customers = df["CustomerID"].nunique()
avg_order_value = df["TotalSales"].mean()
repeat_customers = (df["CustomerID"].value_counts() > 1).sum()
repeat_rate = repeat_customers / unique_customers * 100

# ----------------------------------------------------------------------
# 4. SALES TREND / GROUPBY ANALYSIS
# ----------------------------------------------------------------------
monthly_sales = df.groupby("OrderMonth")["TotalSales"].sum().sort_index()
category_sales = df.groupby("ProductCategory")["TotalSales"].sum().sort_values(ascending=False)
region_sales = df.groupby("Region")["TotalSales"].sum().sort_values(ascending=False)
payment_counts = df["PaymentMethod"].value_counts()
top_category = category_sales.idxmax()
top_region = region_sales.idxmax()

corr_matrix = df[numeric_cols].corr().round(2)

# ----------------------------------------------------------------------
# 5. VISUALIZATIONS
# ----------------------------------------------------------------------

# --- Chart 1: Monthly sales trend (line) ---
plt.figure(figsize=(11, 5))
monthly_sales.plot(kind="line", marker="o", color="#2563eb")
plt.title("Monthly Sales Trend (2024-2025)")
plt.xlabel("Month")
plt.ylabel("Total Sales (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visuals/01_monthly_sales_trend.png")
plt.close()

# --- Chart 2: Revenue by category (bar) ---
plt.figure(figsize=(9, 5.5))
sns.barplot(x=category_sales.values, y=category_sales.index, hue=category_sales.index,
            palette="Blues_r", legend=False)
plt.title("Total Revenue by Product Category")
plt.xlabel("Total Sales (₹)")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig("visuals/02_revenue_by_category.png")
plt.close()

# --- Chart 3: Revenue by region (bar) ---
plt.figure(figsize=(7, 5))
sns.barplot(x=region_sales.index, y=region_sales.values, hue=region_sales.index,
            palette="viridis", legend=False)
plt.title("Total Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales (₹)")
plt.tight_layout()
plt.savefig("visuals/03_revenue_by_region.png")
plt.close()

# --- Chart 4: Distribution of order values (histogram) ---
plt.figure(figsize=(8, 5))
sns.histplot(df["TotalSales"], bins=40, kde=True, color="#16a34a")
plt.title("Distribution of Order Values")
plt.xlabel("Order Value (₹)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("visuals/04_order_value_distribution.png")
plt.close()

# --- Chart 5: Customer age distribution (histogram) ---
plt.figure(figsize=(8, 5))
sns.histplot(df["Age"], bins=25, kde=True, color="#f97316")
plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("visuals/05_customer_age_distribution.png")
plt.close()

# --- Chart 6: Correlation heatmap ---
plt.figure(figsize=(7.5, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("Correlation Heatmap (Numeric Features)")
plt.tight_layout()
plt.savefig("visuals/06_correlation_heatmap.png")
plt.close()

# --- Chart 7: Payment method share (bar) ---
plt.figure(figsize=(8, 5))
sns.barplot(x=payment_counts.values, y=payment_counts.index, hue=payment_counts.index,
            palette="mako", legend=False)
plt.title("Orders by Payment Method")
plt.xlabel("Number of Orders")
plt.ylabel("Payment Method")
plt.tight_layout()
plt.savefig("visuals/07_payment_method_share.png")
plt.close()

print("\nAll charts saved to visuals/")

# ----------------------------------------------------------------------
# 6. SAVE KEY METRICS
# ----------------------------------------------------------------------
stats_summary = {
    "total_revenue": round(float(total_revenue), 2),
    "total_orders": int(total_orders),
    "unique_customers": int(unique_customers),
    "avg_order_value": round(float(avg_order_value), 2),
    "repeat_customers": int(repeat_customers),
    "repeat_rate_pct": round(float(repeat_rate), 2),
    "top_category": top_category,
    "top_category_revenue": round(float(category_sales.max()), 2),
    "top_region": top_region,
    "top_region_revenue": round(float(region_sales.max()), 2),
    "best_month": monthly_sales.idxmax(),
    "best_month_revenue": round(float(monthly_sales.max()), 2),
    "corr_quantity_totalsales": float(corr_matrix.loc["Quantity", "TotalSales"]),
    "corr_discount_satisfaction": float(corr_matrix.loc["DiscountPercent", "CustomerSatisfaction"]),
    "corr_unitprice_totalsales": float(corr_matrix.loc["UnitPrice", "TotalSales"]),
    "category_sales": category_sales.round(2).to_dict(),
    "region_sales": region_sales.round(2).to_dict(),
    "payment_counts": payment_counts.to_dict(),
}

with open("stats.json", "w") as f:
    json.dump(stats_summary, f, indent=2)

desc_stats.to_csv("descriptive_stats.csv")
corr_matrix.to_csv("correlation_matrix.csv")

print("\nKey stats saved to stats.json")
print(json.dumps(stats_summary, indent=2))
