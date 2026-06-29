"""
Script: clean_data.py
Purpose: Clean all raw CSV files and save to data/cleaned/
Preserves raw originals — never overwrites source data.
"""

import pandas as pd
import os
from datetime import datetime

RAW_DIR = r"C:\Users\Mohan\Downloads\sample\data\raw"
CLEAN_DIR = r"C:\Users\Mohan\Downloads\sample\data\cleaned"

os.makedirs(CLEAN_DIR, exist_ok=True)

cleaning_log = []

def log(msg):
    print(f"  >> {msg}")
    cleaning_log.append(msg)

# ============================================================
# 1. CUSTOMERS
# ============================================================
print("\n" + "=" * 60)
print("CLEANING: Customers.csv")
print("=" * 60)

cust = pd.read_csv(os.path.join(RAW_DIR, "Customers.csv"), encoding="latin1")
before = len(cust)
log(f"Loaded {len(cust)} rows, {len(cust.columns)} columns")

# Convert Birthday to datetime
cust["Birthday"] = pd.to_datetime(cust["Birthday"], errors="coerce")
bad_dates = cust["Birthday"].isna().sum()
if bad_dates > 0:
    log(f"WARNING: {bad_dates} birthdays could not be parsed (set to NaT)")

# Handle missing State Code (10 missing = 0.1%)
missing_state_code = cust["State Code"].isna().sum()
cust["State Code"] = cust["State Code"].fillna("Unknown")
if missing_state_code > 0:
    log(f"State Code: filled {missing_state_code} missing values with 'Unknown'")

# Check duplicates
dupes = cust.duplicated().sum()
if dupes > 0:
    cust = cust.drop_duplicates()
    log(f"Removed {dupes} duplicate rows")
else:
    log("No duplicate rows found")

after = len(cust)
log(f"Final: {after} rows (removed {before - after})")

# Save
cust.to_csv(os.path.join(CLEAN_DIR, "Customers.csv"), index=False)
log("Saved to data/cleaned/Customers.csv")
print(cust.dtypes.to_string())
print(cust.head(3).to_string(index=False))


# ============================================================
# 2. PRODUCTS
# ============================================================
print("\n" + "=" * 60)
print("CLEANING: Products.csv")
print("=" * 60)

prod = pd.read_csv(os.path.join(RAW_DIR, "Products.csv"))
before = len(prod)
log(f"Loaded {len(prod)} rows, {len(prod.columns)} columns")

# Clean Unit Cost USD — remove $ and commas, convert to float
log("Cleaning 'Unit Cost USD' — removing '$' and commas, converting to float")
prod["Unit Cost USD"] = (
    prod["Unit Cost USD"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
    .astype(float)
)

# Clean Unit Price USD
log("Cleaning 'Unit Price USD' — removing '$' and commas, converting to float")
prod["Unit Price USD"] = (
    prod["Unit Price USD"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
    .astype(float)
)

# Check for any conversion issues
cost_nulls = prod["Unit Cost USD"].isna().sum()
price_nulls = prod["Unit Price USD"].isna().sum()
if cost_nulls > 0:
    log(f"WARNING: {cost_nulls} null values in Unit Cost USD after conversion")
if price_nulls > 0:
    log(f"WARNING: {price_nulls} null values in Unit Price USD after conversion")

# Check duplicates
dupes = prod.duplicated().sum()
if dupes > 0:
    prod = prod.drop_duplicates()
    log(f"Removed {dupes} duplicate rows")
else:
    log("No duplicate rows found")

after = len(prod)
log(f"Final: {after} rows (removed {before - after})")

# Save
prod.to_csv(os.path.join(CLEAN_DIR, "Products.csv"), index=False)
log("Saved to data/cleaned/Products.csv")
print(prod.dtypes.to_string())
print(prod.head(3).to_string(index=False))


# ============================================================
# 3. STORES
# ============================================================
print("\n" + "=" * 60)
print("CLEANING: Stores.csv")
print("=" * 60)

stores = pd.read_csv(os.path.join(RAW_DIR, "Stores.csv"))
before = len(stores)
log(f"Loaded {len(stores)} rows, {len(stores.columns)} columns")

# Convert Open Date to datetime
stores["Open Date"] = pd.to_datetime(stores["Open Date"], errors="coerce")
bad_dates = stores["Open Date"].isna().sum()
if bad_dates > 0:
    log(f"WARNING: {bad_dates} Open Dates could not be parsed (set to NaT)")

# Handle 1 missing Square Meters (Online store — no physical footprint)
missing_sqm = stores["Square Meters"].isna().sum()
stores["Square Meters"] = stores["Square Meters"].fillna(0.0)
if missing_sqm > 0:
    log(f"Square Meters: filled {missing_sqm} missing value with 0.0 (Online store)")

# Check duplicates
dupes = stores.duplicated().sum()
if dupes > 0:
    stores = stores.drop_duplicates()
    log(f"Removed {dupes} duplicate rows")
else:
    log("No duplicate rows found")

after = len(stores)
log(f"Final: {after} rows (removed {before - after})")

# Save
stores.to_csv(os.path.join(CLEAN_DIR, "Stores.csv"), index=False)
log("Saved to data/cleaned/Stores.csv")
print(stores.dtypes.to_string())
print(stores.head(3).to_string(index=False))


# ============================================================
# 4. SALES
# ============================================================
print("\n" + "=" * 60)
print("CLEANING: Sales.csv")
print("=" * 60)

sales = pd.read_csv(os.path.join(RAW_DIR, "Sales.csv"))
before = len(sales)
log(f"Loaded {len(sales)} rows, {len(sales.columns)} columns")

# Convert Order Date to datetime
sales["Order Date"] = pd.to_datetime(sales["Order Date"], errors="coerce")
bad_order_dates = sales["Order Date"].isna().sum()
if bad_order_dates > 0:
    log(f"WARNING: {bad_order_dates} Order Dates could not be parsed")

# Convert Delivery Date to datetime
sales["Delivery Date"] = pd.to_datetime(sales["Delivery Date"], errors="coerce")
missing_delivery = sales["Delivery Date"].isna().sum()
pct_missing = missing_delivery / len(sales) * 100
log(f"Delivery Date: {missing_delivery} missing ({pct_missing:.1f}%) — left as NaT (not yet delivered / not recorded)")

# Check duplicates
dupes = sales.duplicated().sum()
if dupes > 0:
    sales = sales.drop_duplicates()
    log(f"Removed {dupes} duplicate rows")
else:
    log("No duplicate rows found")

# Verify StoreKey = 0 is in Stores (Online store)
store_keys_in_stores = pd.read_csv(os.path.join(CLEAN_DIR, "Stores.csv"))["StoreKey"].unique()
unknown_stores = sales[~sales["StoreKey"].isin(store_keys_in_stores)]["StoreKey"].unique()
if len(unknown_stores) > 0:
    log(f"WARNING: Sales contains StoreKeys not in Stores table: {unknown_stores}")
else:
    log("All StoreKeys in Sales have a matching Store in Stores table (including Online, key=0)")

after = len(sales)
log(f"Final: {after} rows (removed {before - after})")

# Save
sales.to_csv(os.path.join(CLEAN_DIR, "Sales.csv"), index=False)
log("Saved to data/cleaned/Sales.csv")
print(sales.dtypes.to_string())
print(sales.head(3).to_string(index=False))


# ============================================================
# 5. EXCHANGE RATES
# ============================================================
print("\n" + "=" * 60)
print("CLEANING: Exchange_Rates.csv")
print("=" * 60)

fx = pd.read_csv(os.path.join(RAW_DIR, "Exchange_Rates.csv"))
before = len(fx)
log(f"Loaded {len(fx)} rows, {len(fx.columns)} columns")

# Convert Date to datetime
fx["Date"] = pd.to_datetime(fx["Date"], errors="coerce")
bad_dates = fx["Date"].isna().sum()
if bad_dates > 0:
    log(f"WARNING: {bad_dates} dates could not be parsed")

# Ensure Exchange is numeric
fx["Exchange"] = pd.to_numeric(fx["Exchange"], errors="coerce")
bad_exchange = fx["Exchange"].isna().sum()
if bad_exchange > 0:
    log(f"WARNING: {bad_exchange} Exchange rates could not be converted to numeric")

# Check duplicates
dupes = fx.duplicated().sum()
if dupes > 0:
    fx = fx.drop_duplicates()
    log(f"Removed {dupes} duplicate rows")
else:
    log("No duplicate rows found")

after = len(fx)
log(f"Final: {after} rows (removed {before - after})")

# Save
fx.to_csv(os.path.join(CLEAN_DIR, "Exchange_Rates.csv"), index=False)
log("Saved to data/cleaned/Exchange_Rates.csv")
print(fx.dtypes.to_string())
print(fx.head(3).to_string(index=False))


# ============================================================
# 6. DATA DICTIONARY — pass through (no cleaning needed)
# ============================================================
print("\n" + "=" * 60)
print("COPYING: Data_Dictionary.csv (no cleaning needed)")
print("=" * 60)

dd = pd.read_csv(os.path.join(RAW_DIR, "Data_Dictionary.csv"))
dd.to_csv(os.path.join(CLEAN_DIR, "Data_Dictionary.csv"), index=False)
log("Copied as-is to data/cleaned/Data_Dictionary.csv")


# ============================================================
# SUMMARY REPORT
# ============================================================
print("\n" + "=" * 60)
print("CLEANING SUMMARY REPORT")
print("=" * 60)
for entry in cleaning_log:
    print(f"  - {entry}")
print(f"\nAll cleaned files saved to: {CLEAN_DIR}")
print("Done.")
