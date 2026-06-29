"""
Analysis 1: Revenue Analysis
Uses Unit Price USD from Products as revenue basis.
Revenue = Quantity * Unit Price USD (already in USD)
Cost = Quantity * Unit Cost USD
Profit = Revenue - Cost
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

BASE = r"C:\Users\Mohan\Downloads\sample"
CLEAN_DIR = os.path.join(BASE, "data", "cleaned")
FIGURE_DIR = os.path.join(BASE, "reports", "figures")
os.makedirs(FIGURE_DIR, exist_ok=True)
sns.set_style("whitegrid")

# Load
sales = pd.read_csv(os.path.join(CLEAN_DIR, "Sales.csv"))
prod = pd.read_csv(os.path.join(CLEAN_DIR, "Products.csv"))
stores = pd.read_csv(os.path.join(CLEAN_DIR, "Stores.csv"))
cust = pd.read_csv(os.path.join(CLEAN_DIR, "Customers.csv"))

sales["Order Date"] = pd.to_datetime(sales["Order Date"])

# Merge sales with products (Unit Price USD and Unit Cost USD are already in USD)
sf = sales.merge(prod[["ProductKey", "Category", "Subcategory", "Product Name", "Unit Cost USD", "Unit Price USD"]],
                 on="ProductKey", how="left")
sf = sf.merge(stores[["StoreKey", "Country"]], on="StoreKey", how="left", suffixes=("", "_store"))
sf = sf.merge(cust[["CustomerKey", "Gender"]], on="CustomerKey", how="left")

# Revenue and cost calculations
sf["Revenue_USD"] = sf["Quantity"] * sf["Unit Price USD"]
sf["Cost_USD"] = sf["Quantity"] * sf["Unit Cost USD"]
sf["Profit_USD"] = sf["Revenue_USD"] - sf["Cost_USD"]

total_revenue = sf["Revenue_USD"].sum()
total_cost = sf["Cost_USD"].sum()
total_profit = sf["Profit_USD"].sum()
total_orders = sf["Order Number"].nunique()
total_units = sf["Quantity"].sum()
margin_pct = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0

print("REVENUE ANALYSIS")
print(f"  Total Revenue: ${total_revenue:,.2f}")
print(f"  Total Cost: ${total_cost:,.2f}")
print(f"  Total Profit: ${total_profit:,.2f}")
print(f"  Total Orders: {total_orders:,}")
print(f"  Total Units: {total_units:,}")
print(f"  Overall Margin: {margin_pct:.1f}%")

# Revenue by Category
cat_rev = sf.groupby("Category").agg(
    Revenue=("Revenue_USD", "sum"),
    Cost=("Cost_USD", "sum"),
    Profit=("Profit_USD", "sum"),
    Units=("Quantity", "sum"),
    Orders=("Order Number", "nunique")
).sort_values("Revenue", ascending=False)
cat_rev["Margin%"] = (cat_rev["Profit"] / cat_rev["Revenue"] * 100).round(1)

# Revenue by Country
country_rev = sf.groupby("Country").agg(
    Revenue=("Revenue_USD", "sum"),
    Orders=("Order Number", "nunique")
).sort_values("Revenue", ascending=False)

# Revenue by Store Type
sf["StoreType"] = np.where(sf["StoreKey"] == 0, "Online", "Physical")
type_rev = sf.groupby("StoreType").agg(
    Revenue=("Revenue_USD", "sum"),
    Orders=("Order Number", "nunique")
)

# Top 10 products by revenue
top_prod_rev = sf.groupby(["ProductKey", "Product Name"]).agg(
    Revenue=("Revenue_USD", "sum"),
    Profit=("Profit_USD", "sum"),
    Units=("Quantity", "sum")
).sort_values("Revenue", ascending=False).head(10)

top_cat = cat_rev.index[0]
top_cat_rev = cat_rev.iloc[0]["Revenue"]
top_country = country_rev.index[0]
top_country_rev = country_rev.iloc[0]["Revenue"]
online_pct = type_rev.loc["Online", "Revenue"] / total_revenue * 100 if "Online" in type_rev.index else 0

# Charts
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes[0,0].bar(cat_rev.index, cat_rev["Revenue"] / 1e6, color=sns.color_palette("Set2"))
axes[0,0].set_title("Revenue by Category (Millions USD)")
axes[0,0].tick_params(axis="x", rotation=45)

axes[0,1].bar(country_rev.index, country_rev["Revenue"] / 1e6, color=sns.color_palette("Set3", len(country_rev)))
axes[0,1].set_title("Revenue by Store Country (Millions USD)")
axes[0,1].tick_params(axis="x", rotation=45)

axes[1,0].bar(type_rev.index, type_rev["Revenue"] / 1e6, color=["seagreen", "steelblue"])
axes[1,0].set_title("Revenue: Online vs Physical (Millions USD)")

# Use reset_index to properly access Product Name
top_prod_flat = top_prod_rev.reset_index()
axes[1,1].barh(top_prod_flat["Product Name"].str[:30].iloc[::-1],
               (top_prod_flat["Revenue"] / 1e3).iloc[::-1], color="coral")
axes[1,1].set_title("Top 10 Products by Revenue (Thousands USD)")

plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "a1_revenue_overview.png"), dpi=100)
plt.close()
print("  Chart: a1_revenue_overview.png")

# Margin chart
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["green" if v > 0 else "red" for v in cat_rev["Margin%"]]
ax.bar(cat_rev.index, cat_rev["Margin%"], color=colors)
ax.set_title("Profit Margin % by Category")
ax.set_ylabel("Margin %")
ax.tick_params(axis="x", rotation=45)
ax.axhline(0, color="black", linewidth=0.5)
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "a1_margin_by_category.png"), dpi=100)
plt.close()
print("  Chart: a1_margin_by_category.png")

# Report
lines = []
lines.append("# Revenue Analysis Report")
lines.append("")
lines.append("## Overview")
lines.append("")
lines.append(f"- **Total Revenue:** ${total_revenue:,.2f}")
lines.append(f"- **Total Cost:** ${total_cost:,.2f}")
lines.append(f"- **Total Profit:** ${total_profit:,.2f}")
lines.append(f"- **Overall Margin:** {margin_pct:.1f}%")
lines.append(f"- **Total Orders:** {total_orders:,}")
lines.append(f"- **Total Units Sold:** {total_units:,}")
lines.append(f"- **Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
lines.append("")
lines.append("*Note: Revenue = Quantity x Unit Price USD (from Products). Profit = Revenue - Cost.*")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Revenue by Category")
lines.append("")
lines.append("| Category | Revenue (USD) | Cost (USD) | Profit (USD) | Margin % | Units | Orders |")
lines.append("|---|---|---|---|---|---|---|")
for cat, row in cat_rev.iterrows():
    lines.append(f"| {cat} | ${row['Revenue']:,.2f} | ${row['Cost']:,.2f} | ${row['Profit']:,.2f} | {row['Margin%']}% | {row['Units']:,} | {row['Orders']:,} |")

lines.append("")
lines.append("## Revenue by Store Country")
lines.append("")
lines.append("| Country | Revenue (USD) | Orders |")
lines.append("|---|---|---|")
for c, row in country_rev.iterrows():
    lines.append(f"| {c} | ${row['Revenue']:,.2f} | {row['Orders']:,} |")

lines.append("")
lines.append("## Online vs Physical")
lines.append("")
lines.append("| Store Type | Revenue (USD) | Orders |")
lines.append("|---|---|---|")
for t, row in type_rev.iterrows():
    lines.append(f"| {t} | ${row['Revenue']:,.2f} | {row['Orders']:,} |")

lines.append("")
lines.append("## Top 10 Products by Revenue")
lines.append("")
lines.append("| Product | Revenue (USD) | Profit (USD) | Units |")
lines.append("|---|---|---|---|")
for _, row in top_prod_flat.iterrows():
    lines.append(f"| {row['Product Name']} | ${row['Revenue']:,.2f} | ${row['Profit']:,.2f} | {row['Units']:,} |")

lines.append("")
lines.append("## Charts")
lines.append("")
lines.append("- `reports/figures/a1_revenue_overview.png`")
lines.append("- `reports/figures/a1_margin_by_category.png`")
lines.append("")
lines.append("## Key Insights")
lines.append("")
lines.append(f"- **{top_cat}** is the top revenue category at ${top_cat_rev:,.2f}")
lines.append(f"- **{top_country}** generates the most revenue (${top_country_rev:,.2f})")
lines.append(f"- Online channel contributes **{online_pct:.1f}%** of total revenue")

best_margin_name = cat_rev["Margin%"].idxmax()
best_margin_val = cat_rev.loc[best_margin_name, "Margin%"]
lines.append(f"- **{best_margin_name}** has the highest margin at {best_margin_val}%")

with open(os.path.join(BASE, "reports", "revenue-analysis-report.md"), "w") as f:
    f.write("\n".join(lines))
print("  Report: reports/revenue-analysis-report.md")
print("REVENUE ANALYSIS COMPLETE\n")
