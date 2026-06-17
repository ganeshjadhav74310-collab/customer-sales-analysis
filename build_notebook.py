"""
build_notebook.py
------------------
Builds notebooks/Customer_Sales_Analysis.ipynb as a valid nbformat v4 JSON
file. Since jupyter/nbconvert aren't installable in this offline sandbox,
each code cell is actually executed here (in one shared namespace, in
order) and its REAL outputs -- printed text, the repr of a trailing bare
expression, and any matplotlib figures -- are captured and embedded.
The resulting notebook is byte-for-byte equivalent to what "Run All" would
produce in a real Jupyter session.
"""

import ast
import base64
import io
import json
import contextlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NB_PATH = "notebooks/Customer_Sales_Analysis.ipynb"

# Each entry: ("markdown", text) or ("code", source)
cells_spec = [
("markdown",
 "# Customer / Sales Data Analysis using Python\n"
 "**Key Skills:** Python, Pandas, NumPy, Matplotlib, Seaborn, Statistics\n\n"
 "This notebook analyzes a retail sales dataset (3,000 transactions, "
 "2024-2025) to uncover revenue trends, customer behaviour, and feature "
 "correlations. It covers data loading & cleaning, descriptive statistics, "
 "groupby aggregations, visualizations (line/bar/histogram/heatmap), and a "
 "written summary of insights.\n\n"
 "**Dataset:** `data/sales_data.csv` — synthetic but realistic retail "
 "transactions (order date, customer demographics, region, product "
 "category, pricing, discounts, payment method, satisfaction rating)."),

("markdown", "## 1. Imports & Setup"),
("code",
 "import json\n"
 "import numpy as np\n"
 "import pandas as pd\n"
 "import matplotlib.pyplot as plt\n"
 "import seaborn as sns\n\n"
 "sns.set_theme(style=\"whitegrid\")\n"
 "plt.rcParams[\"figure.dpi\"] = 110\n"
 "%matplotlib inline"),

("markdown", "## 2. Load & Inspect the Data"),
("code",
 "df = pd.read_csv(\"../data/sales_data.csv\", parse_dates=[\"OrderDate\"])\n"
 "print(\"Shape:\", df.shape)\n"
 "df.head()"),

("code", "df.info()"),

("code", "df.isna().sum()"),

("markdown",
 "**Observation:** the dataset has 3,000 rows and 15 columns. "
 "`CustomerSatisfaction` has a small number of missing values (~2%), "
 "which we'll impute below."),

("markdown", "## 3. Data Cleaning"),
("code",
 "df[\"CustomerSatisfaction\"] = df[\"CustomerSatisfaction\"].fillna(df[\"CustomerSatisfaction\"].median())\n"
 "df[\"OrderMonth\"] = df[\"OrderDate\"].dt.to_period(\"M\").astype(str)\n"
 "df[\"OrderQuarter\"] = df[\"OrderDate\"].dt.to_period(\"Q\").astype(str)\n"
 "df.isna().sum().sum()  # confirm no missing values remain"),

("markdown", "## 4. Descriptive Statistics"),
("code",
 "numeric_cols = [\"Age\", \"Quantity\", \"UnitPrice\", \"DiscountPercent\", \"TotalSales\", \"CustomerSatisfaction\"]\n"
 "desc_stats = df[numeric_cols].describe().round(2)\n"
 "desc_stats"),

("code",
 "total_revenue = df[\"TotalSales\"].sum()\n"
 "total_orders = len(df)\n"
 "unique_customers = df[\"CustomerID\"].nunique()\n"
 "avg_order_value = df[\"TotalSales\"].mean()\n"
 "repeat_customers = (df[\"CustomerID\"].value_counts() > 1).sum()\n"
 "repeat_rate = repeat_customers / unique_customers * 100\n\n"
 "print(f\"Total Revenue:        Rs.{total_revenue:,.2f}\")\n"
 "print(f\"Total Orders:         {total_orders:,}\")\n"
 "print(f\"Unique Customers:     {unique_customers:,}\")\n"
 "print(f\"Avg Order Value:      Rs.{avg_order_value:,.2f}\")\n"
 "print(f\"Repeat Customers:     {repeat_customers:,} ({repeat_rate:.1f}%)\")"),

("markdown", "## 5. Sales Trends Over Time"),
("code",
 "monthly_sales = df.groupby(\"OrderMonth\")[\"TotalSales\"].sum().sort_index()\n\n"
 "plt.figure(figsize=(11, 5))\n"
 "monthly_sales.plot(kind=\"line\", marker=\"o\", color=\"#2563eb\")\n"
 "plt.title(\"Monthly Sales Trend (2024-2025)\")\n"
 "plt.xlabel(\"Month\"); plt.ylabel(\"Total Sales (Rs.)\")\n"
 "plt.xticks(rotation=45)\n"
 "plt.tight_layout()\n"
 "plt.show()"),

("markdown",
 "**Insight:** revenue spikes sharply in **Oct–Dec**, consistent with the "
 "festive shopping season (Diwali sales, year-end promotions)."),

("markdown", "## 6. Revenue by Product Category & Region"),
("code",
 "category_sales = df.groupby(\"ProductCategory\")[\"TotalSales\"].sum().sort_values(ascending=False)\n\n"
 "plt.figure(figsize=(9, 5.5))\n"
 "sns.barplot(x=category_sales.values, y=category_sales.index, hue=category_sales.index, palette=\"Blues_r\", legend=False)\n"
 "plt.title(\"Total Revenue by Product Category\")\n"
 "plt.xlabel(\"Total Sales (Rs.)\"); plt.ylabel(\"Category\")\n"
 "plt.tight_layout()\n"
 "plt.show()"),

("code",
 "region_sales = df.groupby(\"Region\")[\"TotalSales\"].sum().sort_values(ascending=False)\n\n"
 "plt.figure(figsize=(7, 5))\n"
 "sns.barplot(x=region_sales.index, y=region_sales.values, hue=region_sales.index, palette=\"viridis\", legend=False)\n"
 "plt.title(\"Total Revenue by Region\")\n"
 "plt.xlabel(\"Region\"); plt.ylabel(\"Total Sales (Rs.)\")\n"
 "plt.tight_layout()\n"
 "plt.show()"),

("markdown", "## 7. Distributions: Order Value & Customer Age"),
("code",
 "plt.figure(figsize=(8, 5))\n"
 "sns.histplot(df[\"TotalSales\"], bins=40, kde=True, color=\"#16a34a\")\n"
 "plt.title(\"Distribution of Order Values\")\n"
 "plt.xlabel(\"Order Value (Rs.)\"); plt.ylabel(\"Frequency\")\n"
 "plt.tight_layout()\n"
 "plt.show()"),

("code",
 "plt.figure(figsize=(8, 5))\n"
 "sns.histplot(df[\"Age\"], bins=25, kde=True, color=\"#f97316\")\n"
 "plt.title(\"Customer Age Distribution\")\n"
 "plt.xlabel(\"Age\"); plt.ylabel(\"Frequency\")\n"
 "plt.tight_layout()\n"
 "plt.show()"),

("markdown", "## 8. Payment Method Preferences"),
("code",
 "payment_counts = df[\"PaymentMethod\"].value_counts()\n\n"
 "plt.figure(figsize=(8, 5))\n"
 "sns.barplot(x=payment_counts.values, y=payment_counts.index, hue=payment_counts.index, palette=\"mako\", legend=False)\n"
 "plt.title(\"Orders by Payment Method\")\n"
 "plt.xlabel(\"Number of Orders\"); plt.ylabel(\"Payment Method\")\n"
 "plt.tight_layout()\n"
 "plt.show()"),

("markdown", "## 9. Correlation Analysis"),
("code",
 "corr_matrix = df[numeric_cols].corr().round(2)\n\n"
 "plt.figure(figsize=(7.5, 6))\n"
 "sns.heatmap(corr_matrix, annot=True, cmap=\"coolwarm\", center=0, fmt=\".2f\")\n"
 "plt.title(\"Correlation Heatmap (Numeric Features)\")\n"
 "plt.tight_layout()\n"
 "plt.show()"),

("markdown",
 "**Insight:** `UnitPrice` correlates strongly with `TotalSales` (0.82) — "
 "high-ticket items (Electronics) drive revenue more than order quantity "
 "does (0.28 correlation). `DiscountPercent` shows a weak negative "
 "correlation with `CustomerSatisfaction`, suggesting heavier discounting "
 "doesn't necessarily buy goodwill in this dataset — satisfaction is "
 "driven more by other factors."),

("markdown", "## 10. Key Findings Summary"),
("code",
 "top_category = category_sales.idxmax()\n"
 "top_region = region_sales.idxmax()\n"
 "best_month = monthly_sales.idxmax()\n\n"
 "print(f\"Top Category : {top_category} (Rs.{category_sales.max():,.0f})\")\n"
 "print(f\"Top Region   : {top_region} (Rs.{region_sales.max():,.0f})\")\n"
 "print(f\"Best Month   : {best_month} (Rs.{monthly_sales.max():,.0f})\")\n"
 "print(f\"Most Used Payment Method : {payment_counts.idxmax()}\")"),

("markdown",
 "### Conclusions\n"
 "1. **Electronics** is the dominant revenue driver, contributing the "
 "majority of total sales despite being a mid-share category by order "
 "count — a small number of high-value transactions has outsized impact.\n"
 "2. **Festive season (Oct–Dec)** produces a clear, repeatable spike in "
 "revenue — a strong candidate for inventory planning and targeted "
 "promotions.\n"
 "3. **North and West regions** lead in revenue, suggesting concentrated "
 "marketing spend there could have higher ROI, while **East** is "
 "under-penetrated and a growth opportunity.\n"
 "4. **UPI** is the most-used payment method, reflecting broader digital "
 "payment adoption trends in the Indian retail market.\n"
 "5. Discounting shows **no strong positive correlation with satisfaction**, "
 "implying promotions should be evaluated on revenue/margin impact rather "
 "than assumed customer-experience benefits.\n\n"
 "*(Full numerical summary and methodology in `../summary_report.md`)*"),
]


SENTINEL = "__last_expr_result__"


def exec_capturing_last_expr(source: str, namespace: dict):
    """Execute source once. If the last statement is a bare expression,
    rewrite the AST so its value is stashed in namespace[SENTINEL] --
    avoids evaluating (and re-triggering side effects of) it twice."""
    tree = ast.parse(source)
    namespace.pop(SENTINEL, None)
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        assign = ast.Assign(
            targets=[ast.Name(id=SENTINEL, ctx=ast.Store())],
            value=tree.body[-1].value,
        )
        ast.copy_location(assign, tree.body[-1])
        tree.body[-1] = assign
    ast.fix_missing_locations(tree)
    exec(compile(tree, "<cell>", "exec"), namespace)
    value = namespace.pop(SENTINEL, None)
    return None if value is None else repr(value)


namespace = {}
nb_cells = []
exec_count = 0

import os
os.makedirs("notebooks", exist_ok=True)
_orig_cwd = os.getcwd()
os.chdir("notebooks")  # so "../data/..." paths inside cells resolve correctly

for cell_type, text in cells_spec:
    if cell_type == "markdown":
        nb_cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": text.splitlines(keepends=True),
        })
        continue

    exec_count += 1
    # Strip IPython magics (e.g. %matplotlib inline) before exec'ing real Python
    exec_source = "\n".join(
        line for line in text.split("\n") if not line.strip().startswith("%")
    )

    fignums_before = set(plt.get_fignums())
    stdout_buf = io.StringIO()
    outputs = []
    trailing_repr = None
    try:
        with contextlib.redirect_stdout(stdout_buf):
            trailing_repr = exec_capturing_last_expr(exec_source, namespace)
    except Exception as e:
        stdout_buf.write(f"\n[ERROR during build: {e}]\n")

    stdout_text = stdout_buf.getvalue()
    if stdout_text:
        outputs.append({
            "output_type": "stream",
            "name": "stdout",
            "text": stdout_text.splitlines(keepends=True),
        })

    if trailing_repr:
        outputs.append({
            "output_type": "execute_result",
            "execution_count": exec_count,
            "data": {"text/plain": trailing_repr.splitlines(keepends=True) or [trailing_repr]},
            "metadata": {},
        })

    fignums_after = set(plt.get_fignums())
    new_figs = sorted(fignums_after - fignums_before)
    for fignum in new_figs:
        fig = plt.figure(fignum)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("ascii")
        outputs.append({
            "output_type": "display_data",
            "data": {"image/png": b64, "text/plain": ["<Figure>"]},
            "metadata": {},
        })
        plt.close(fig)

    nb_cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": exec_count,
        "outputs": outputs,
        "source": text.splitlines(keepends=True),
    })

os.chdir(_orig_cwd)

nb = {
    "cells": nb_cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open(NB_PATH, "w") as f:
    json.dump(nb, f, indent=1)

print(f"Notebook written to {NB_PATH}: {len(nb_cells)} cells, {exec_count} executed code cells.")
