"""
generate_data.py
-----------------
Generates a realistic synthetic retail sales dataset for the
Customer / Sales Data Analysis project.

The dataset simulates ~24 months of e-commerce/retail transactions
with customer demographics, product categories, regional spread,
seasonality (festive-season boost in Oct-Dec), and pricing/discount
behaviour so that the analysis notebook has genuine patterns to find.
"""

import numpy as np
import pandas as pd

RNG_SEED = 42
N_RECORDS = 3000
START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

rng = np.random.default_rng(RNG_SEED)

# ---- Reference data -------------------------------------------------
cities_by_region = {
    "North": ["Delhi", "Jaipur", "Lucknow", "Chandigarh"],
    "South": ["Bangalore", "Chennai", "Hyderabad", "Kochi"],
    "West": ["Mumbai", "Pune", "Ahmedabad", "Surat"],
    "East": ["Kolkata", "Patna", "Bhubaneswar", "Guwahati"],
}
region_list = list(cities_by_region.keys())

categories = {
    "Electronics": {
        "products": ["Wireless Earbuds", "Smartphone", "Laptop", "Smartwatch", "Bluetooth Speaker"],
        "price_range": (1200, 65000),
    },
    "Clothing": {
        "products": ["T-Shirt", "Jeans", "Jacket", "Saree", "Sneakers"],
        "price_range": (400, 4500),
    },
    "Home & Kitchen": {
        "products": ["Mixer Grinder", "Non-stick Pan", "Bedsheet Set", "Air Fryer", "Water Bottle"],
        "price_range": (300, 9000),
    },
    "Books": {
        "products": ["Fiction Novel", "Self-Help Book", "Comic Book", "Textbook", "Cookbook"],
        "price_range": (150, 1200),
    },
    "Beauty & Personal Care": {
        "products": ["Face Wash", "Perfume", "Hair Dryer", "Lipstick", "Sunscreen"],
        "price_range": (150, 3500),
    },
    "Sports & Fitness": {
        "products": ["Yoga Mat", "Dumbbell Set", "Cricket Bat", "Running Shoes", "Resistance Bands"],
        "price_range": (300, 6000),
    },
    "Groceries": {
        "products": ["Rice (5kg)", "Cooking Oil", "Snack Pack Combo", "Tea/Coffee Pack", "Spice Combo"],
        "price_range": (100, 1500),
    },
}
category_list = list(categories.keys())
# Roughly mimics real-world category demand share
category_weights = np.array([0.22, 0.18, 0.15, 0.08, 0.12, 0.10, 0.15])
category_weights = category_weights / category_weights.sum()

payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"]
payment_weights = [0.35, 0.22, 0.18, 0.10, 0.15]

# ---- Helper: seasonal weighting for order dates ----------------------
all_days = pd.date_range(START_DATE, END_DATE, freq="D")
month_boost = {10: 1.6, 11: 1.9, 12: 1.7}  # festive season boost (Oct-Dec)
day_weights = np.array([month_boost.get(d.month, 1.0) for d in all_days], dtype=float)
day_weights = day_weights / day_weights.sum()

order_dates = rng.choice(all_days, size=N_RECORDS, p=day_weights)

# ---- Generate customers (some repeat customers, some one-time) -------
N_CUSTOMERS = 1200
customer_ids = [f"CUST{str(i).zfill(5)}" for i in range(1, N_CUSTOMERS + 1)]
customer_age = rng.normal(34, 11, size=N_CUSTOMERS).clip(18, 70).round().astype(int)
customer_gender = rng.choice(["Male", "Female", "Other"], size=N_CUSTOMERS, p=[0.52, 0.46, 0.02])
customer_region = rng.choice(region_list, size=N_CUSTOMERS, p=[0.27, 0.28, 0.27, 0.18])
customer_city = [rng.choice(cities_by_region[r]) for r in customer_region]

customers_df = pd.DataFrame({
    "CustomerID": customer_ids,
    "Age": customer_age,
    "Gender": customer_gender,
    "Region": customer_region,
    "City": customer_city,
})

# Some customers order more than once (loyal customers) -> sample with repetition,
# loyal customers (first 200) get higher sampling weight
cust_weights = np.ones(N_CUSTOMERS)
cust_weights[:200] *= 4.0
cust_weights = cust_weights / cust_weights.sum()
chosen_customers = rng.choice(customer_ids, size=N_RECORDS, p=cust_weights)

# ---- Build transactions ----------------------------------------------
rows = []
for i in range(N_RECORDS):
    cust_id = chosen_customers[i]
    cust_row = customers_df.loc[customers_df.CustomerID == cust_id].iloc[0]

    category = rng.choice(category_list, p=category_weights)
    cat_info = categories[category]
    product = rng.choice(cat_info["products"])
    low, high = cat_info["price_range"]
    unit_price = round(rng.uniform(low, high), 2)

    quantity = int(rng.choice([1, 2, 3, 4, 5], p=[0.45, 0.25, 0.15, 0.10, 0.05]))
    # Festive months see slightly higher discounts (promotions)
    order_date = pd.Timestamp(order_dates[i])
    base_discount = rng.choice([0, 5, 10, 15, 20, 25], p=[0.30, 0.25, 0.20, 0.13, 0.08, 0.04])
    if order_date.month in (10, 11, 12):
        base_discount = min(base_discount + rng.choice([0, 5, 10]), 40)
    discount_pct = base_discount

    gross = unit_price * quantity
    total_sales = round(gross * (1 - discount_pct / 100), 2)

    payment = rng.choice(payment_methods, p=payment_weights)
    satisfaction = int(np.clip(rng.normal(4.0 - discount_pct * 0.01, 0.9), 1, 5).round())

    rows.append({
        "OrderID": f"ORD{str(i+1).zfill(5)}",
        "OrderDate": order_date.date().isoformat(),
        "CustomerID": cust_id,
        "Age": int(cust_row["Age"]),
        "Gender": cust_row["Gender"],
        "Region": cust_row["Region"],
        "City": cust_row["City"],
        "ProductCategory": category,
        "Product": product,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "DiscountPercent": discount_pct,
        "TotalSales": total_sales,
        "PaymentMethod": payment,
        "CustomerSatisfaction": satisfaction,
    })

df = pd.DataFrame(rows)

# Introduce a small amount of realistic messiness (missing values) for cleaning practice
missing_idx = rng.choice(df.index, size=int(0.02 * N_RECORDS), replace=False)
df.loc[missing_idx, "CustomerSatisfaction"] = np.nan

df = df.sort_values("OrderDate").reset_index(drop=True)
df.to_csv("data/sales_data.csv", index=False)

print(f"Generated {len(df)} records -> data/sales_data.csv")
print(df.head())
