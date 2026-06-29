"""
Investigate StoreKey = 0 in Sales
"""
import pandas as pd

sales = pd.read_csv(r"C:\Users\Mohan\Downloads\sample\data\raw\Sales.csv")
stores = pd.read_csv(r"C:\Users\Mohan\Downloads\sample\data\raw\Stores.csv")

print("=" * 60)
print("INVESTIGATING StoreKey = 0 IN SALES")
print("=" * 60)

zero_stores = sales[sales["StoreKey"] == 0]
print(f"Rows with StoreKey = 0: {len(zero_stores)}")
print(f"Unique Order Numbers: {zero_stores['Order Number'].nunique()}")
print(f"Currency Codes:\n  {zero_stores['Currency Code'].value_counts().to_string()}")
print(f"Date range: {zero_stores['Order Date'].min()} to {zero_stores['Order Date'].max()}")
print(f"Unique Customers: {zero_stores['CustomerKey'].nunique()}")
print(f"Unique Products: {zero_stores['ProductKey'].nunique()}")

print("\nIs StoreKey 0 in Stores table?")
print(f"  0 in Stores: {0 in stores['StoreKey'].values}")

print("\nStores available:")
print(stores[["StoreKey", "Country", "State"]].head(10).to_string(index=False))
print(f"... total {len(stores)} stores, keys {stores['StoreKey'].min()} to {stores['StoreKey'].max()}")
