"""
Analysis 2: Customer Segmentation (RFM)
Generates reports/customer-segmentation-report.md + charts
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
fx["Date"] = pd.to_datetime(fx["Date"])
cust["Birthday"] = pd.to_datetime(cust["Birthday"])
cust["Age"] = (datetime(2020, 12, 31) - cust["Birthday"]).dt.days / 365.25

# Merge sales with Products for Unit Price USD (revenue basis in USD)
sales_rev = sales.merge(prod[["ProductKey", "Unit Price USD"]], on="ProductKey", how="left").copy()
sales_rev["Revenue_USD"] = sales_rev["Quantity"] * sales_rev["Unit Price USD"]

# RFM
max_date = sales_rev["Order Date"].max()
ref_date = max_date + pd.Timedelta(days=1)

rfm = sales_rev.groupby("CustomerKey").agg(
    Recency=("Order Date", lambda x: (ref_date - x.max()).days),
    Frequency=("Order Number", "nunique"),
    Monetary=("Revenue_USD", "sum")
).reset_index()

rfm = rfm.merge(cust[["CustomerKey", "Gender", "Age", "State", "City", "Country", "Continent"]], on="CustomerKey", how="left")

# Scores (1-4, higher is better)
rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4, 3, 2, 1])
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4])
rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 4, labels=[1, 2, 3, 4])

rfm["RFM_Score"] = rfm["R_Score"].astype(int) + rfm["F_Score"].astype(int) + rfm["M_Score"].astype(int)

def segment(s):
    if s >= 10: return "Champions"
    if s >= 8: return "Loyal"
    if s >= 6: return "Potential"
    if s >= 4: return "At Risk"
    return "Lost"

rfm["Segment"] = rfm["RFM_Score"].apply(segment)

seg_summary = rfm.groupby("Segment", observed=False).agg(
    Customers=("CustomerKey", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum")
).round(1).sort_values("Avg_Monetary", ascending=False)

top_customers = rfm.sort_values("Monetary", ascending=False).head(10)
seg_gender = rfm.groupby(["Segment", "Gender"], observed=False).size().unstack(fill_value=0)
seg_age = rfm.groupby("Segment", observed=False)["Age"].agg(["mean", "min", "max"]).round(1)

print("CUSTOMER SEGMENTATION (RFM)")
print(f"  Customers analyzed: {len(rfm):,}")
print(f"  Segments: {list(seg_summary.index)}")

# Charts
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].bar(seg_summary.index, seg_summary["Customers"], color=sns.color_palette("Set2"))
axes[0].set_title("Customer Segments by Count")
axes[0].set_ylabel("Customers")
axes[1].bar(seg_summary.index, seg_summary["Total_Revenue"] / 1e6, color=sns.color_palette("Set3"))
axes[1].set_title("Revenue by Segment (Millions USD)")
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "a2_customer_segments.png"), dpi=100)
plt.close()
print("  Chart: a2_customer_segments.png")

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(top_customers["CustomerKey"].astype(str), top_customers["Monetary"] / 1e3, color="steelblue")
ax.set_title("Top 10 Customers by Revenue")
ax.set_xlabel("Revenue (Thousands USD)")
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "a2_top_customers.png"), dpi=100)
plt.close()
print("  Chart: a2_top_customers.png")

# Report
lines = []
lines.append("# Customer Segmentation Report (RFM Analysis)")
lines.append("")
lines.append("## Overview")
lines.append("")
lines.append(f"- **Total Customers Analyzed:** {len(rfm):,}")
lines.append(f"- **Reference Date:** {ref_date.strftime('%Y-%m-%d')}")
lines.append("- **Method:** RFM (Recency, Frequency, Monetary) scored 1-4 each")
lines.append("")
lines.append("## Segment Summary")
lines.append("")
lines.append("| Segment | Customers | Avg Recency (days) | Avg Frequency | Avg Spend ($) | Total Revenue ($) |")
lines.append("|---|---|---|---|---|---|")
for seg, row in seg_summary.iterrows():
    lines.append(f"| {seg} | {row['Customers']:,} | {row['Avg_Recency']:.0f} | {row['Avg_Frequency']:.1f} | ${row['Avg_Monetary']:,.2f} | ${row['Total_Revenue']:,.2f} |")

lines.append("")
lines.append("## Segment Descriptions")
lines.append("")
lines.append("| Segment | Description | Action |")
lines.append("|---|---|---|")
lines.append("| **Champions** | Bought recently, often, and spend most | Reward & nurture |")
lines.append("| **Loyal** | Regular customers, good spend | Upsell & cross-sell |")
lines.append("| **Potential** | Moderate recency/frequency/spend | Grow relationship |")
lines.append("| **At Risk** | Used to buy but haven't recently | Re-engage campaigns |")
lines.append("| **Lost** | Long time since last purchase, low spend | Win-back or ignore |")

lines.append("")
lines.append("## Top 10 Customers by Revenue")
lines.append("")
lines.append("| Customer ID | Revenue ($) | Frequency | Recency (days) | Segment | Gender | Age |")
lines.append("|---|---|---|---|---|---|---|")
for _, row in top_customers.iterrows():
    lines.append(f"| {row['CustomerKey']} | ${row['Monetary']:,.2f} | {row['Frequency']} | {row['Recency']} | {row['Segment']} | {row['Gender']} | {row['Age']:.0f} |")

lines.append("")
lines.append("## Charts")
lines.append("")
lines.append("- `reports/figures/a2_customer_segments.png`")
lines.append("- `reports/figures/a2_top_customers.png`")

lines.append("")
lines.append("## Key Insights")
lines.append("")
top_seg = seg_summary.index[0]
lines.append(f"- **{top_seg}** segment has the highest avg spend (${seg_summary.iloc[0]['Avg_Monetary']:,.2f})")
largest_seg = seg_summary.sort_values("Customers", ascending=False).index[0]
lines.append(f"- **{largest_seg}** is the largest segment ({seg_summary.loc[largest_seg, 'Customers']:,} customers)")
lines.append(f"- Top 10 customers: ${top_customers['Monetary'].sum():,.2f} in total revenue")

with open(os.path.join(BASE, "reports", "customer-segmentation-report.md"), "w") as f:
    f.write("\n".join(lines))
print("  Report: reports/customer-segmentation-report.md")
print("CUSTOMER SEGMENTATION COMPLETE\n")
