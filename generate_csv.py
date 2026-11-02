import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

PRODUCTS = [
    ("PROD001", "iPhone 15 Pro", "Electronics", 999.00, 650.00),
    ("PROD002", "Samsung Galaxy S24", "Electronics", 799.00, 520.00),
    ("PROD003", "MacBook Air M3", "Electronics", 1299.00, 900.00),
    ("PROD004", "Sony WH-1000XM5", "Electronics", 349.00, 180.00),
    ("PROD005", "Nike Air Max", "Footwear", 129.00, 55.00),
    ("PROD006", "Adidas Ultraboost", "Footwear", 189.00, 80.00),
    ("PROD007", "Levi's 501 Jeans", "Apparel", 89.00, 35.00),
    ("PROD008", "North Face Jacket", "Apparel", 249.00, 110.00),
    ("PROD009", "KitchenAid Mixer", "Home and Kitchen", 449.00, 220.00),
    ("PROD010", "Instant Pot", "Home and Kitchen", 99.00, 45.00),
    ("PROD011", "Harry Potter Box Set", "Books", 89.00, 28.00),
    ("PROD012", "Atomic Habits", "Books", 18.00, 6.00),
    ("PROD013", "Yoga Mat Premium", "Sports", 79.00, 25.00),
    ("PROD014", "Protein Powder 5lb", "Health", 59.00, 22.00),
    ("PROD015", "AirPods Pro 2", "Electronics", 249.00, 140.00),
]

REGIONS = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"]
STORES = [f"STORE_{i:03d}" for i in range(1, 21)]
CUSTOMERS = [f"CUST_{i:04d}" for i in range(1, 251)]

def get_seasonal_multiplier(d):
    month = d.month
    day_of_week = d.weekday()
    base = 1.0
    if month == 12:
        base *= 2.2
    elif month == 11:
        base *= 1.7
    elif month in [6, 7]:
        base *= 1.25
    elif month in [1, 2]:
        base *= 0.8
    if day_of_week >= 5:
        base *= 1.2
    return base

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
num_days = (end_date - start_date).days

records = []
for day_offset in range(num_days + 1):
    current_date = start_date + timedelta(days=day_offset)
    seasonal = get_seasonal_multiplier(current_date)
    daily_orders = int(np.random.poisson(9 * seasonal))
    if daily_orders < 1:
        daily_orders = 1

    for _ in range(daily_orders):
        p = random.choice(PRODUCTS)
        region = random.choices(REGIONS, weights=[40, 25, 20, 10, 5])[0]
        store = random.choice(STORES)
        customer = random.choice(CUSTOMERS)

        qty = max(1, int(np.random.lognormal(0.4, 0.6)))
        unit_price = round(p[3] * np.random.uniform(0.9, 1.1), 2)
        unit_cost = round(p[4] * np.random.uniform(0.95, 1.05), 2)
        revenue = round(qty * unit_price, 2)
        cost = round(qty * unit_cost, 2)
        profit = round(revenue - cost, 2)

        records.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "product_name": p[1],
            "category": p[2],
            "region": region,
            "quantity": qty,
            "unit_price": unit_price,
            "revenue": revenue,
            "cost": cost,
            "profit": profit,
            "customer_id": customer,
            "store_id": store,
            "product_id": p[0],
        })

df = pd.DataFrame(records).sort_values("date").reset_index(drop=True)

# Save both in root and in data directory
output_file_root = "sample_sales_upload.csv"
output_file_data = "data/sample_sales_upload.csv"
df.to_csv(output_file_root, index=False)
df.to_csv(output_file_data, index=False)

print(f"Successfully generated {len(df):,} rows.")
print(f"File 1: {output_file_root}")
print(f"File 2: {output_file_data}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Total revenue: ${df['revenue'].sum():,.2f}")
print(f"Total profit: ${df['profit'].sum():,.2f}")
print(f"Unique customers: {df['customer_id'].nunique()}")
print(f"Unique products: {df['product_name'].nunique()}")
