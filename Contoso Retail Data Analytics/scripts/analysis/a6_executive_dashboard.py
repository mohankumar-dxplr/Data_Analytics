"""
Analysis 6: Executive Dashboard
Generates reports/executive-dashboard-report.md + chart
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
cust = pd.read_csv(os.path.join(CLEAN_DIR, "Customers.csv"))
prod = pd.read_csv(os.path.join(CLEAN_DIR, "Products.csv"))
stores = pd.read_csv(os.path.join(CLEAN_DIR, "Stores.csv"))
sales = pd.read_csv(os.path.join(CLEAN_DIR, "Sales.csv"))
fx = pd.read_csv(os.path.join(CLEAN_DIR, "Exchange_Rates.csv"))

sales["Order Date"] = pd.to_datetime(sales["Order Date"])
sales["Delivery Date"] = pd.to_datetime(sales["Delivery Date"])
fx["Date"] = pd.to_datetime(fx["Date"])
cust["Birthday"] = pd.to_datetime(cust["Birthday"])

# Merge for product info and revenue calculation
sales_rev = sales.merge(prod[["ProductKey", "Category", "Subcategory", "Product Name", "Unit Cost USD", "Unit Price USD"]], on="ProductKey", how="left")
sales_rev["Revenue_USD"] = sales_rev["Quantity"] * sales_rev["Unit Price USD"]
sales_rev["Cost_USD"] = sales_rev["Quantity"] * sales_rev["Unit Cost USD"]
sales_rev["Margin_USD"] = sales_rev["Revenue_USD"] - sales_rev["Cost_USD"]
sales_rev = sales_rev.merge(stores[["StoreKey", "Country"]], on="StoreKey", how="left", suffixes=("", "_store"))
sales_rev["StoreType"] = np.where(sales_rev["StoreKey"] == 0, "Online", "Physical")

total_revenue = sales_rev["Revenue_USD"].sum()
total_orders = sales_rev["Order Number"].nunique()
total_units = sales_rev["Quantity"].sum()

total_margin = sales_rev["Margin_USD"].sum()
margin_pct = total_margin / total_revenue * 100

# Category revenue
cat_rev = sales_rev.groupby("Category")["Revenue_USD"].sum().sort_values(ascending=False)
top_cat = cat_rev.index[0]
top_cat_rev = cat_rev.iloc[0]

# Country revenue
country_rev = sales_rev.groupby("Country")["Revenue_USD"].sum().sort_values(ascending=False)
top_country = country_rev.index[0]
top_country_rev = country_rev.iloc[0]

# Store type
type_rev = sales_rev.groupby("StoreType")["Revenue_USD"].sum()
online_pct = type_rev.get("Online", 0) / total_revenue * 100

# Top 5 products
top_prod_rev = sales_rev.groupby(["ProductKey", "Product Name"]).agg(
    Revenue=("Revenue_USD", "sum"),
    Units=("Quantity", "sum")
).sort_values("Revenue", ascending=False).head(5).reset_index()

# Monthly for trend
monthly = sales_rev.set_index("Order Date").resample("ME")["Revenue_USD"].sum().reset_index()

# Delivery
delivered = sales.dropna(subset=["Delivery Date"]).copy()
delivered["Delivery_Days"] = (delivered["Delivery Date"] - delivered["Order Date"]).dt.days
deliv_store = delivered.merge(stores[["StoreKey", "Country"]], on="StoreKey", how="left")
deliv_store["StoreType"] = np.where(deliv_store["StoreKey"] == 0, "Online", "Physical")
avg_del = deliv_store["Delivery_Days"].mean()
type_del = deliv_store.groupby("StoreType")["Delivery_Days"].mean()
delivery_pct_val = len(delivered) / len(sales) * 100

# Customer segments (RFM)
rfm = sales_rev.groupby("CustomerKey").agg(
    Recency=("Order Date", lambda x: (sales_rev["Order Date"].max() + pd.Timedelta(days=1) - x.max()).days),
    Frequency=("Order Number", "nunique"),
    Monetary=("Revenue_USD", "sum")
).reset_index()

# Yearly
yearly = sales_rev.set_index("Order Date").resample("YE")["Revenue_USD"].sum().reset_index()

print("EXECUTIVE DASHBOARD")
print(f"  Total Revenue: ${total_revenue:,.2f}")

# Dashboard chart
fig = plt.figure(figsize=(16, 12))
ax1 = plt.subplot(3, 3, (1, 4))
ax1.plot(monthly["Order Date"], monthly["Revenue_USD"] / 1e6, color="navy", linewidth=2, marker="o", markersize=3)
ax1.set_title("Monthly Revenue (Millions USD)", fontsize=13, fontweight="bold")
ax1.tick_params(axis="x", rotation=45)

ax2 = plt.subplot(3, 3, 3)
ax2.pie(cat_rev.values, labels=cat_rev.index, autopct="%1.0f%%", startangle=90, colors=sns.color_palette("Set3"))
ax2.set_title("Revenue by Category", fontsize=11, fontweight="bold")

ax3 = plt.subplot(3, 3, 6)
ax3.pie(type_rev.values, labels=type_rev.index, autopct="%1.0f%%", startangle=90, colors=["seagreen", "steelblue"])
ax3.set_title("Online vs Physical", fontsize=11, fontweight="bold")

ax4 = plt.subplot(3, 3, 7)
# Quick segment classification
rfm["Segment"] = pd.cut(rfm["Monetary"], bins=[0, rfm["Monetary"].quantile(0.25), rfm["Monetary"].quantile(0.5), rfm["Monetary"].quantile(0.75), rfm["Monetary"].max()],
                         labels=["Low", "Medium", "High", "VIP"])
seg_counts = rfm["Segment"].value_counts()
ax4.bar(seg_counts.index, seg_counts.values, color=sns.color_palette("Set2"))
ax4.set_title("Customer Value Segments", fontsize=11, fontweight="bold")

ax5 = plt.subplot(3, 3, 8)
rev_k = top_prod_rev["Revenue"] / 1e3
ax5.barh(top_prod_rev["Product Name"].str[:25].iloc[::-1], rev_k.iloc[::-1], color="coral")
ax5.set_title("Top 5 Products (Thousands USD)", fontsize=11, fontweight="bold")

ax6 = plt.subplot(3, 3, 9)
ax6.bar(type_del.index, type_del.values, color=["seagreen", "steelblue"])
ax6.set_title("Avg Delivery Time (days)", fontsize=11, fontweight="bold")

plt.suptitle("Contoso Retail -- Executive Dashboard", fontsize=18, fontweight="bold", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(FIGURE_DIR, "a6_executive_dashboard.png"), dpi=100)
plt.close()
print("  Chart: a6_executive_dashboard.png")

# Report
lines = []
lines.append("# Executive Dashboard Report")
lines.append("")
lines.append("## Key Performance Indicators (KPIs)")
lines.append("")
lines.append("| Metric | Value |")
lines.append("|---|---|")
lines.append(f"| **Total Revenue** | ${total_revenue:,.2f} |")
lines.append(f"| **Total Orders** | {total_orders:,} |")
lines.append(f"| **Total Units Sold** | {total_units:,} |")
lines.append(f"| **Total Profit** | ${total_margin:,.2f} |")
lines.append(f"| **Overall Margin** | {margin_pct:.1f}% |")
lines.append(f"| **Active Customers** | {len(rfm):,} |")
lines.append(f"| **Top Category** | {top_cat} (${top_cat_rev:,.2f}) |")
lines.append(f"| **Top Country** | {top_country} (${top_country_rev:,.2f}) |")
lines.append(f"| **Online Revenue Share** | {online_pct:.1f}% |")
lines.append(f"| **Average Delivery Time** | {avg_del:.1f} days |")

lines.append("")
lines.append("## Revenue by Category")
lines.append("")
lines.append("| Category | Revenue (USD) | % of Total |")
lines.append("|---|---|---|")
for cat, rev in cat_rev.items():
    lines.append(f"| {cat} | ${rev:,.2f} | {rev/total_revenue*100:.1f}% |")

lines.append("")
lines.append("## Revenue by Store Country")
lines.append("")
lines.append("| Country | Revenue (USD) | % of Total |")
lines.append("|---|---|---|")
for c, rev in country_rev.items():
    lines.append(f"| {c} | ${rev:,.2f} | {rev/total_revenue*100:.1f}% |")

lines.append("")
lines.append("## Year-over-Year Growth")
lines.append("")
lines.append("| Year | Revenue (USD) | Growth |")
lines.append("|---|---|---|")
for i, (_, row) in enumerate(yearly.iterrows()):
    if i == 0:
        g = "-"
    else:
        g = f"{(row['Revenue_USD'] - yearly.iloc[i-1]['Revenue_USD']) / yearly.iloc[i-1]['Revenue_USD'] * 100:+.1f}%"
    lines.append(f"| {row['Order Date'].year} | ${row['Revenue_USD']:,.2f} | {g} |")

lines.append("")
lines.append("## Top 5 Products by Revenue")
lines.append("")
lines.append("| Product | Revenue (USD) | Units Sold |")
lines.append("|---|---|---|")
for _, row in top_prod_rev.iterrows():
    lines.append(f"| {row['Product Name']} | ${row['Revenue']:,.2f} | {row['Units']:,} |")

lines.append("")
lines.append("## Delivery Performance")
lines.append("")
lines.append(f"- Orders with delivery data: {len(delivered):,} ({delivery_pct_val:.1f}%)")
lines.append(f"- Average delivery time: {avg_del:.1f} days")
if "Online" in type_del.index:
    lines.append(f"- Online avg delivery: {type_del['Online']:.1f} days")
if "Physical" in type_del.index:
    lines.append(f"- Physical avg delivery: {type_del['Physical']:.1f} days")

lines.append("")
lines.append("## Chart")
lines.append("")
lines.append("- `reports/figures/a6_executive_dashboard.png`")
lines.append("")
lines.append("## Recommendations")
lines.append("")
lines.append(f"1. **Focus on {top_cat}** -- top revenue category at ${top_cat_rev:,.2f}")
lines.append(f"2. **Grow online channel** -- currently {online_pct:.1f}% of revenue")
lines.append(f"3. **Target VIP & High-value customers** -- upsell opportunities")
lines.append(f"4. **Improve delivery tracking** -- only {delivery_pct_val:.1f}% of orders have delivery data")

with open(os.path.join(BASE, "reports", "executive-dashboard-report.md"), "w") as f:
    f.write("\n".join(lines))
print("  Report: reports/executive-dashboard-report.md")
print("EXECUTIVE DASHBOARD COMPLETE\n")
