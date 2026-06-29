"""
Script: eda_cleaned_data.py
Purpose: Exploratory Data Analysis on all cleaned datasets.
Generates summary stats, distributions, and visualizations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

CLEAN_DIR = r"C:\Users\Mohan\Downloads\sample\data\cleaned"
REPORT_DIR = r"C:\Users\Mohan\Downloads\sample\reports\figures"
os.makedirs(REPORT_DIR, exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

print("=" * 70)
print("  EXPLORATORY DATA ANALYSIS")
print("=" * 70)

# Load all data
print("\nLoading cleaned datasets...")
cust = pd.read_csv(os.path.join(CLEAN_DIR, "Customers.csv"))
prod = pd.read_csv(os.path.join(CLEAN_DIR, "Products.csv"))
stores = pd.read_csv(os.path.join(CLEAN_DIR, "Stores.csv"))
sales = pd.read_csv(os.path.join(CLEAN_DIR, "Sales.csv"))
fx = pd.read_csv(os.path.join(CLEAN_DIR, "Exchange_Rates.csv"))

# Convert dates
for col in ["Birthday"]:
    cust[col] = pd.to_datetime(cust[col])
stores["Open Date"] = pd.to_datetime(stores["Open Date"])
sales["Order Date"] = pd.to_datetime(sales["Order Date"])
sales["Delivery Date"] = pd.to_datetime(sales["Delivery Date"])
fx["Date"] = pd.to_datetime(fx["Date"])

# Customer age
today = datetime(2020, 12, 31)
cust["Age"] = (today - cust["Birthday"]).dt.days / 365.25

print("Done.\n")

# ============================================================
# 1. CUSTOMERS
# ============================================================
print("#" * 60)
print("# 1. CUSTOMERS")
print("#" * 60)

print(f"\n  Shape: {cust.shape[0]:,} rows, {cust.shape[1]} columns")
print(f"  Gender: Male={cust['Gender'].value_counts().get('Male',0):,}, Female={cust['Gender'].value_counts().get('Female',0):,}")
print(f"  Age range: {cust['Age'].min():.0f} - {cust['Age'].max():.0f} years (median: {cust['Age'].median():.0f})")
print(f"  Countries: {cust['Country'].nunique()} — {list(cust['Country'].unique())}")
print(f"  Continents: {cust['Continent'].nunique()} — {list(cust['Continent'].unique())}")
print(f"  Top 5 cities: {dict(cust['City'].value_counts().head(5).to_dict())}")
print(f"  Missing values: {cust.isnull().sum().sum()}")

# Chart 1: Age distribution
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(cust["Age"].dropna(), bins=40, color="steelblue", edgecolor="white")
ax.set_title("Customer Age Distribution")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "01_customers_age_gender.png"), dpi=100)
plt.close()
print("  Chart: 01_customers_age_gender.png")

# Chart 2: Top 15 states
top_states = cust["State"].value_counts().head(15)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(y=top_states.index, x=top_states.values, hue=top_states.index, palette="viridis", legend=False, ax=ax)
ax.set_title("Top 15 States by Customer Count")
ax.set_xlabel("Customers")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "02_customers_top_states.png"), dpi=100)
plt.close()
print("  Chart: 02_customers_top_states.png")


# ============================================================
# 2. PRODUCTS
# ============================================================
print("\n" + "#" * 60)
print("# 2. PRODUCTS")
print("#" * 60)

print(f"\n  Shape: {prod.shape[0]:,} rows, {prod.shape[1]} columns")
print(f"  Categories ({prod['Category'].nunique()}): {dict(prod['Category'].value_counts().to_dict())}")
print(f"  Brands: {list(prod['Brand'].unique())}")
print(f"  Unit Price range: ${prod['Unit Price USD'].min():.2f} - ${prod['Unit Price USD'].max():.2f}")
print(f"  Median Unit Price: ${prod['Unit Price USD'].median():.2f}")
print(f"  Margin (Price - Cost) range: ${(prod['Unit Price USD']-prod['Unit Cost USD']).min():.2f} - ${(prod['Unit Price USD']-prod['Unit Cost USD']).max():.2f}")
print(f"  Missing values: {prod.isnull().sum().sum()}")

# Chart 3: Category distribution + Price
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
cat_counts = prod["Category"].value_counts()
axes[0].bar(cat_counts.index, cat_counts.values, color=sns.color_palette("Set2"))
axes[0].set_title("Products by Category")
axes[0].tick_params(axis="x", rotation=45)
axes[1].hist(prod["Unit Price USD"], bins=40, color="coral", edgecolor="white", alpha=0.7)
axes[1].axvline(prod["Unit Price USD"].median(), color="red", ls="--", label=f"Median=${prod['Unit Price USD'].median():.2f}")
axes[1].set_title("Unit Price Distribution")
axes[1].set_xlabel("Price (USD)")
axes[1].legend()
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "03_products_category_price.png"), dpi=100)
plt.close()
print("  Chart: 03_products_category_price.png")

# Chart 4: Cost vs Price
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(prod["Unit Cost USD"], prod["Unit Price USD"], alpha=0.4, s=10, color="green")
max_val = max(prod["Unit Price USD"].max(), prod["Unit Cost USD"].max())
ax.plot([0, max_val], [0, max_val], "r--", alpha=0.5, label="Price = Cost")
ax.set_xlabel("Unit Cost (USD)")
ax.set_ylabel("Unit Price (USD)")
ax.set_title("Product Cost vs Price")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "04_products_cost_vs_price.png"), dpi=100)
plt.close()
print("  Chart: 04_products_cost_vs_price.png")


# ============================================================
# 3. STORES
# ============================================================
print("\n" + "#" * 60)
print("# 3. STORES")
print("#" * 60)

print(f"\n  Shape: {stores.shape[0]} rows, {stores.shape[1]} columns")
print(f"  Countries ({stores['Country'].nunique()}): {dict(stores['Country'].value_counts().to_dict())}")
phys_stores = stores[stores["Square Meters"] > 0]
print(f"  Physical stores: {len(phys_stores)} (avg {phys_stores['Square Meters'].mean():.0f} sqm)")
print(f"  Online store: 1 (Square Meters = 0)")
print(f"  Open Date range: {stores['Open Date'].min().date()} to {stores['Open Date'].max().date()}")
print(f"  Missing values: {stores.isnull().sum().sum()}")

# Chart 5: Stores by country and size
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
country_counts = stores["Country"].value_counts()
axes[0].bar(country_counts.index, country_counts.values, color=sns.color_palette("Set3", len(country_counts)))
axes[0].set_title("Stores by Country")
axes[0].tick_params(axis="x", rotation=45)
axes[1].hist(phys_stores["Square Meters"], bins=15, color="teal", edgecolor="white")
axes[1].set_title("Physical Store Size (sq meters)")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "05_stores_country_size.png"), dpi=100)
plt.close()
print("  Chart: 05_stores_country_size.png")


# ============================================================
# 4. SALES
# ============================================================
print("\n" + "#" * 60)
print("# 4. SALES")
print("#" * 60)

print(f"\n  Shape: {sales.shape[0]:,} rows, {sales.shape[1]} columns")
print(f"  Order Date range: {sales['Order Date'].min().date()} to {sales['Order Date'].max().date()}")
print(f"  Total unique orders: {sales['Order Number'].nunique():,}")
print(f"  Currencies: {dict(sales['Currency Code'].value_counts().to_dict())}")
print(f"  Online (Store=0): {(sales['StoreKey']==0).sum():,} rows ({(sales['StoreKey']==0).mean()*100:.1f}%)")
print(f"  Physical stores: {(sales['StoreKey']!=0).sum():,} rows ({(sales['StoreKey']!=0).mean()*100:.1f}%)")
print(f"  Quantity range: {sales['Quantity'].min()} - {sales['Quantity'].max()}")
print(f"  Missing values: Delivery Date = {sales['Delivery Date'].isna().sum():,} ({sales['Delivery Date'].isna().mean()*100:.1f}%)")

# Chart 6: Monthly orders
sales["YearMonth"] = sales["Order Date"].dt.to_period("M")
monthly_orders = sales.groupby("YearMonth").size()
monthly_idx = monthly_orders.index.to_timestamp()

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
axes[0,0].plot(monthly_idx, monthly_orders.values, color="navy", linewidth=1)
axes[0,0].set_title("Monthly Order Count")
axes[0,0].tick_params(axis="x", rotation=45)

curr_counts = sales["Currency Code"].value_counts()
axes[0,1].pie(curr_counts.values, labels=curr_counts.index, autopct="%1.1f%%", colors=sns.color_palette("Set3"))
axes[0,1].set_title("Orders by Currency")

axes[1,0].hist(sales["Quantity"], bins=range(1, 25), color="darkorange", edgecolor="white")
axes[1,0].set_title("Quantity per Order")

bar_vals = [(sales["StoreKey"]==0).sum(), (sales["StoreKey"]!=0).sum()]
axes[1,1].bar(["Online", "Physical"], bar_vals, color=["seagreen", "steelblue"])
axes[1,1].set_title("Online vs Physical Orders")

plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "06_sales_overview.png"), dpi=100)
plt.close()
print("  Chart: 06_sales_overview.png")


# ============================================================
# 5. EXCHANGE RATES
# ============================================================
print("\n" + "#" * 60)
print("# 5. EXCHANGE RATES")
print("#" * 60)

print(f"\n  Shape: {fx.shape[0]:,} rows, {fx.shape[1]} columns")
print(f"  Date range: {fx['Date'].min().date()} to {fx['Date'].max().date()}")
print(f"  Currencies: {sorted(fx['Currency'].unique())}")
print(f"  Days per currency: {fx['Currency'].value_counts().to_dict()}")

# Chart 7: Exchange rates over time
fig, ax = plt.subplots(figsize=(12, 5))
for ccy in sorted(fx["Currency"].unique()):
    if ccy == "USD": continue
    d = fx[fx["Currency"] == ccy]
    ax.plot(d["Date"], d["Exchange"], label=ccy, linewidth=0.8, alpha=0.8)
ax.set_title("Exchange Rates vs USD")
ax.set_ylabel("1 USD = ?")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "07_exchange_rates.png"), dpi=100)
plt.close()
print("  Chart: 07_exchange_rates.png")


# ============================================================
# 6. CROSS-TABLE ANALYSIS
# ============================================================
print("\n" + "#" * 60)
print("# 6. CROSS-TABLE ANALYSIS")
print("#" * 60)

# Merge Sales with Products
sales_prod = sales.merge(prod[["ProductKey", "Category", "Subcategory"]], on="ProductKey", how="left")

# Merge Sales with Customers
sales_cust = sales.merge(cust[["CustomerKey", "Gender", "Age"]], on="CustomerKey", how="left")

# Merge Sales with Stores
sales_store = sales.merge(stores[["StoreKey", "Country"]], on="StoreKey", how="left")

# Category sales
cat_sales = sales_prod.groupby("Category").agg(
    Orders=("Order Number", "nunique"),
    Units=("Quantity", "sum")
).sort_values("Units", ascending=False)
print(f"\n  Sales by Category:\n{cat_sales.to_string()}")

# Top 5 subcategories
top_sub = sales_prod.groupby("Subcategory")["Quantity"].sum().sort_values(ascending=False).head(5)
print(f"\n  Top 5 Subcategories:\n{top_sub.to_string()}")

# Gender sales
gender_sales = sales_cust.groupby("Gender").agg(
    Orders=("Order Number", "nunique"),
    Units=("Quantity", "sum"),
    Customers=("CustomerKey", "nunique")
)
print(f"\n  Sales by Gender:\n{gender_sales.to_string()}")

# Country sales
country_sales = sales_store.groupby("Country").agg(
    Orders=("Order Number", "nunique"),
    Units=("Quantity", "sum")
).sort_values("Orders", ascending=False)
print(f"\n  Sales by Store Country:\n{country_sales.to_string()}")

# Chart 8: Category + Gender
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
cat_sales["Units"].plot(kind="bar", ax=axes[0], color=sns.color_palette("Set2"))
axes[0].set_title("Units Sold by Category")
axes[0].tick_params(axis="x", rotation=45)
gender_sales["Units"].plot(kind="bar", ax=axes[1], color=["lightcoral", "lightskyblue"])
axes[1].set_title("Units Sold by Customer Gender")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "08_cross_category_gender.png"), dpi=100)
plt.close()
print("  Chart: 08_cross_category_gender.png")

# Chart 9: Top subcategories
fig, ax = plt.subplots(figsize=(10, 5))
top_sub.plot(kind="barh", color="teal", ax=ax)
ax.set_title("Top 5 Subcategories by Units Sold")
ax.set_xlabel("Total Units")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "09_top_subcategories.png"), dpi=100)
plt.close()
print("  Chart: 09_top_subcategories.png")

# Age group analysis
cust["AgeGroup"] = pd.cut(cust["Age"], bins=[0, 20, 30, 40, 50, 60, 100],
                          labels=["<20", "20-29", "30-39", "40-49", "50-59", "60+"])
age_sales = sales_cust.merge(cust[["CustomerKey", "AgeGroup"]], on="CustomerKey", how="left")
age_grp = age_sales.groupby("AgeGroup", observed=False)["Quantity"].sum()

fig, ax = plt.subplots(figsize=(10, 5))
age_grp.plot(kind="bar", color="coral", ax=ax)
ax.set_title("Units Sold by Customer Age Group")
ax.set_xlabel("Age Group")
ax.set_ylabel("Total Units")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "10_sales_by_age_group.png"), dpi=100)
plt.close()
print("  Chart: 10_sales_by_age_group.png")

# Store type analysis
online_units = sales_store[sales_store["Country"] == "Online"]["Quantity"].sum()
phys_units = sales_store[sales_store["Country"] != "Online"]["Quantity"].sum()
print(f"\n  Online units: {online_units:,} ({online_units/(online_units+phys_units)*100:.1f}%)")
print(f"  Physical units: {phys_units:,} ({phys_units/(online_units+phys_units)*100:.1f}%)")


# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("  EDA SUMMARY")
print("=" * 70)
print(f"""
  DATASETS:
    Customers:      {len(cust):>7,} rows
    Products:       {len(prod):>7,} rows
    Stores:         {len(stores):>7,} rows
    Sales:          {len(sales):>7,} rows
    Exchange Rates: {len(fx):>7,} rows

  KEY METRICS:
    Customer age range:          {cust['Age'].min():.0f} - {cust['Age'].max():.0f} yrs
    Products:                    {len(prod)} products, {prod['Category'].nunique()} categories
    Stores:                      {len(phys_stores)} physical + 1 online
    Sales period:                {sales['Order Date'].min().date()} to {sales['Order Date'].max().date()}
    Online order share:          {(sales['StoreKey']==0).mean()*100:.1f}%
    Delivery recorded:           {(~sales['Delivery Date'].isna()).mean()*100:.1f}%

  TOP CATEGORY:                  {cat_sales.index[0]} ({cat_sales.iloc[0]['Units']:,} units)
  TOP SUBCATEGORY:               {top_sub.index[0]} ({top_sub.iloc[0]:,} units)

  ALL CHARTS SAVED TO:           {REPORT_DIR}
""")

print("EDA complete.")
