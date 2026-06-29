"""
Script: explore_raw_data.py
Purpose: Quick EDA to understand data in the raw folder
"""
import pandas as pd
import os

RAW_DIR = r"C:\Users\Mohan\Downloads\sample\data\raw"
FILES = sorted([f for f in os.listdir(RAW_DIR) if f.endswith(".csv")])

for fname in FILES:
    path = os.path.join(RAW_DIR, fname)
    # Customers.csv has non-UTF-8 characters, use latin1
    encoding = "latin1" if fname == "Customers.csv" else "utf-8"
    df = pd.read_csv(path, encoding=encoding)

    print(f"{'='*60}")
    print(f"  FILE: {fname}")
    print(f"{'='*60}")
    print(f"  Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"  Columns: {list(df.columns)}")
    print(f"\n  Data Types:")
    for col, dtype in df.dtypes.items():
        print(f"    {col}: {dtype}")
    
    print(f"\n  Missing Values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(1)
    for col in df.columns:
        if missing[col] > 0:
            print(f"    {col}: {missing[col]} missing ({missing_pct[col]}%)")
        else:
            print(f"    {col}: 0 missing")
    
    print(f"\n  Duplicate Rows: {df.duplicated().sum()}")

    # Show first 2 rows as a preview
    print(f"\n  First 2 rows:")
    print(df.head(2).to_string(index=False))

    print()

# Additional cross-table observations
print(f"{'='*60}")
print("  CROSS-TABLE OBSERVATIONS")
print(f"{'='*60}")

# Key relationships
print("""
  RELATIONSHIPS BETWEEN TABLES:
    - Sales.CustomerKey  -> Customers.CustomerKey
    - Sales.StoreKey     -> Stores.StoreKey
    - Sales.ProductKey   -> Products.ProductKey
    - Sales.CurrencyCode + Sales.Order Date -> Exchange_Rates.Currency + Exchange_Rates.Date
""")
