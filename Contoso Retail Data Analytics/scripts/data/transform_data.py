import pandas as pd
import numpy as np
from pathlib import Path
import re

CLEAN_DIR = Path(r"C:\Users\Mohan\Downloads\sample\data\cleaned")
TRANSFORM_DIR = Path(r"C:\Users\Mohan\Downloads\sample\data\transformed")
TRANSFORM_DIR.mkdir(exist_ok=True)
ENCODING = "ISO-8859-1"

changes_log = []

def log(step, detail):
    changes_log.append({"step": step, "detail": detail})

# ── Load cleaned data ──
sales = pd.read_csv(CLEAN_DIR / "Sales.csv", encoding=ENCODING, parse_dates=["Order Date", "Delivery Date"])
customers = pd.read_csv(CLEAN_DIR / "Customers.csv", encoding=ENCODING, parse_dates=["Birthday"])
products = pd.read_csv(CLEAN_DIR / "Products.csv", encoding=ENCODING)
stores = pd.read_csv(CLEAN_DIR / "Stores.csv", encoding=ENCODING, parse_dates=["Open Date"])
exchange = pd.read_csv(CLEAN_DIR / "Exchange_Rates.csv", encoding=ENCODING, parse_dates=["Date"])

log("load", f"Loaded {len(sales)} sales, {len(customers)} customers, {len(products)} products, {len(stores)} stores, {len(exchange)} exchange rates")

# ── 1. Feature Engineering on Sales ──

# Merge product info into sales
sales = sales.merge(products[["ProductKey", "Product Name", "Brand", "Color", "Unit Cost USD", "Unit Price USD", "Subcategory", "Category"]], on="ProductKey", how="left")
log("merge", "Merged Products into Sales on ProductKey")

# Merge customer info
sales = sales.merge(customers[["CustomerKey", "Gender", "City", "State", "Country", "Continent", "Birthday"]], on="CustomerKey", how="left", suffixes=("", "_customer"))
log("merge", "Merged Customers into Sales on CustomerKey")

# Merge store info
stores_renamed = stores.rename(columns={"Country": "Store Country", "State": "Store State"})
sales = sales.merge(stores_renamed[["StoreKey", "Store Country", "Store State", "Square Meters"]], on="StoreKey", how="left")
log("merge", "Merged Stores into Sales on StoreKey")

# ── 2. Calculated Fields ──

# Revenue (in original currency)
sales["Revenue"] = sales["Quantity"] * sales["Unit Price USD"]
log("calculate", "Added Revenue = Quantity * Unit Price USD")

# Cost
sales["Cost"] = sales["Quantity"] * sales["Unit Cost USD"]
log("calculate", "Added Cost = Quantity * Unit Cost USD")

# Profit
sales["Profit"] = sales["Revenue"] - sales["Cost"]
log("calculate", "Added Profit = Revenue - Cost")

# Profit Margin
sales["Profit Margin %"] = np.where(sales["Revenue"] > 0, (sales["Profit"] / sales["Revenue"]) * 100, 0)
log("calculate", "Added Profit Margin %")

# Delivery time in days
sales["Delivery Days"] = (sales["Delivery Date"] - sales["Order Date"]).dt.days
long_delivery = (sales["Delivery Days"] > 365).sum()
if long_delivery > 0:
    log("flag", f"Found {long_delivery} orders with delivery > 365 days — possible data issue")
log("calculate", "Added Delivery Days = Delivery Date - Order Date")

# Customer Age at order time
if "Birthday" in sales.columns:
    sales["Customer Age"] = (sales["Order Date"] - sales["Birthday"]).dt.days // 365
    log("calculate", "Added Customer Age at time of order")

# Date-based features
sales["Order Year"] = sales["Order Date"].dt.year
sales["Order Month"] = sales["Order Date"].dt.month
sales["Order Day"] = sales["Order Date"].dt.day
sales["Order Day of Week"] = sales["Order Date"].dt.dayofweek  # 0=Monday
sales["Order Quarter"] = sales["Order Date"].dt.quarter
log("calculate", "Added date features: Year, Month, Day, DayOfWeek, Quarter")

# ── 3. Currency Conversion to USD ──

exchange_pivot = exchange.pivot_table(index="Date", columns="Currency", values="Exchange").reset_index()
exchange_pivot.columns.name = None

# Merge exchange rates for each currency
for currency in ["USD", "CAD", "EUR", "GBP", "AUD"]:
    if currency in exchange_pivot.columns:
        col_name = f"Exchange_{currency}"
        exchange_rates = exchange_pivot[["Date", currency]].rename(columns={currency: col_name})
        sales = sales.merge(exchange_rates, left_on="Order Date", right_on="Date", how="left")
        sales = sales.drop(columns=["Date"])

log("transform", "Merged exchange rates for USD, CAD, EUR, GBP, AUD")

# Convert revenue to USD
def convert_to_usd(row):
    currency = row["Currency Code"]
    rev = row["Revenue"]
    if currency == "USD" or pd.isna(rev):
        return rev
    rate_col = f"Exchange_{currency}"
    rate = row.get(rate_col, np.nan)
    if pd.notna(rate) and rate > 0:
        return rev / rate
    return np.nan

sales["Revenue USD"] = sales.apply(convert_to_usd, axis=1)
log("calculate", "Converted Revenue to USD using daily exchange rates")

# Also convert Cost and Profit to USD
def convert_field_usd(row, field):
    currency = row["Currency Code"]
    val = row[field]
    if currency == "USD" or pd.isna(val):
        return val
    rate_col = f"Exchange_{currency}"
    rate = row.get(rate_col, np.nan)
    if pd.notna(rate) and rate > 0:
        return val / rate
    return np.nan

sales["Cost USD"] = sales.apply(lambda r: convert_field_usd(r, "Cost"), axis=1)
sales["Profit USD"] = sales.apply(lambda r: convert_field_usd(r, "Profit"), axis=1)
log("calculate", "Converted Cost and Profit to USD")

# ── 4. Categorize store type ──
sales["Store Type"] = np.where(sales["StoreKey"] == 0, "Online", "Physical")
log("transform", "Added Store Type (Online vs Physical)")

# ── 5. Price Tier ──
price_tiers = pd.cut(sales["Unit Price USD"], bins=[0, 50, 200, 500, 10000], labels=["Budget", "Mid", "Premium", "Luxury"])
sales["Price Tier"] = price_tiers
log("transform", "Added Price Tier based on Unit Price: Budget (<50), Mid (50-200), Premium (200-500), Luxury (500+)")

# ── Save transformed master table ──
sales.to_csv(TRANSFORM_DIR / "Sales_Enriched.csv", index=False)
log("save", "Saved enriched sales table: Sales_Enriched.csv")

# ── 6. Create aggregated views ──

# Monthly sales by category
monthly_category = sales.groupby(["Order Year", "Order Month", "Category"]).agg(
    Total_Revenue_USD=("Revenue USD", "sum"),
    Total_Profit_USD=("Profit USD", "sum"),
    Order_Count=("Order Number", "nunique"),
    Units_Sold=("Quantity", "sum")
).reset_index()
monthly_category.to_csv(TRANSFORM_DIR / "Monthly_Sales_by_Category.csv", index=False)
log("aggregate", "Created monthly sales by category")

# Sales by country
country_sales = sales.groupby(["Store Country"]).agg(
    Total_Revenue_USD=("Revenue USD", "sum"),
    Total_Profit_USD=("Profit USD", "sum"),
    Order_Count=("Order Number", "nunique")
).reset_index().sort_values("Total_Revenue_USD", ascending=False)
country_sales.to_csv(TRANSFORM_DIR / "Sales_by_Country.csv", index=False)
log("aggregate", "Created sales by country")

# Top 10 products
top_products = sales.groupby("Product Name").agg(
    Total_Revenue_USD=("Revenue USD", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Order_Count=("Order Number", "nunique")
).reset_index().sort_values("Total_Revenue_USD", ascending=False).head(10)
top_products.to_csv(TRANSFORM_DIR / "Top_10_Products.csv", index=False)
log("aggregate", "Created top 10 products by revenue")

# Sales by store type (Online vs Physical)
store_type_sales = sales.groupby("Store Type").agg(
    Total_Revenue_USD=("Revenue USD", "sum"),
    Total_Profit_USD=("Profit USD", "sum"),
    Order_Count=("Order Number", "nunique"),
    Units_Sold=("Quantity", "sum")
).reset_index()
store_type_sales.to_csv(TRANSFORM_DIR / "Sales_by_Store_Type.csv", index=False)
log("aggregate", "Created sales by store type (Online vs Physical)")

# Monthly trend
monthly_trend = sales.groupby(["Order Year", "Order Month"]).agg(
    Total_Revenue_USD=("Revenue USD", "sum"),
    Total_Profit_USD=("Profit USD", "sum"),
    Order_Count=("Order Number", "nunique")
).reset_index().sort_values(["Order Year", "Order Month"])
monthly_trend.to_csv(TRANSFORM_DIR / "Monthly_Trend.csv", index=False)
log("aggregate", "Created monthly revenue/profit trend")

# ── Generate Report ──
report_lines = [
    "# Data Transformation Report",
    "",
    "## Overview",
    "",
    "Applied transformations on cleaned retail data to create enriched analytics-ready datasets.",
    "",
    "## Transformed Files",
    "",
    "| File | Description |",
    "|------|-------------|",
    "| `Sales_Enriched.csv` | Master table: all sales with joined dimensions + calculated fields |",
    "| `Monthly_Sales_by_Category.csv` | Monthly revenue/profit/units by product category |",
    "| `Sales_by_Country.csv` | Revenue/profit by store country |",
    "| `Top_10_Products.csv` | Top 10 products by revenue |",
    "| `Sales_by_Store_Type.csv` | Online vs Physical store comparison |",
    "| `Monthly_Trend.csv` | Monthly revenue & profit time series |",
    "",
    "## Transformations Applied",
    "",
]

for idx, entry in enumerate(changes_log, 1):
    step_icon = {
        "load": "Input",
        "merge": "Join",
        "calculate": "Calc",
        "transform": "Transform",
        "aggregate": "Aggregate",
        "flag": "Flag",
        "save": "Output",
    }.get(entry["step"], entry["step"])
    report_lines.append(f"{idx}. **[{step_icon}]** {entry['detail']}")

report_lines += [
    "",
    "## Key Business Insights Enabled",
    "",
    "- **Revenue in USD**: Multi-currency sales normalized to USD for global comparison",
    "- **Profitability**: Profit and margin calculated at line-item level",
    "- **Customer Demographics**: Age, gender, and location now analyzable per order",
    "- **Delivery Performance**: Delivery days calculated to measure logistics efficiency",
    "- **Time Intelligence**: Date parts extracted for trend, seasonality, and cohort analysis",
    "- **Catalog Analysis**: Price tiers enable segmentation by product value",
    "- **Channel Comparison**: Online vs Physical store performance directly comparable",
    "",
    "## Files Location",
    "",
    "- Raw data: `data/`",
    "- Cleaned data: `cleaned data/`",
    "- Transformed data: `transformed data/`",
]

report = "\n".join(report_lines)
report_path = Path("reports") / "data transformation report.md"
report_path.parent.mkdir(exist_ok=True)
report_path.write_text(report, encoding="utf-8")

print("[OK] Transformations complete")
print(f"[OK] Report: {report_path}")
print(f"\nTransformed files saved in {TRANSFORM_DIR}/:")
for f in sorted(TRANSFORM_DIR.iterdir()):
    print(f"  - {f.name}")
