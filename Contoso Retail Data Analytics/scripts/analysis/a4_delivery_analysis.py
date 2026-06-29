"""
Analysis 4: Delivery & Fulfillment
Generates reports/delivery-analysis-report.md + charts
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

BASE = r"C:\Users\Mohan\Downloads\sample"
CLEAN_DIR = os.path.join(BASE, "data", "cleaned")
FIGURE_DIR = os.path.join(BASE, "reports", "figures")
os.makedirs(FIGURE_DIR, exist_ok=True)
sns.set_style("whitegrid")

sales = pd.read_csv(os.path.join(CLEAN_DIR, "Sales.csv"))
stores = pd.read_csv(os.path.join(CLEAN_DIR, "Stores.csv"))

sales["Order Date"] = pd.to_datetime(sales["Order Date"])
sales["Delivery Date"] = pd.to_datetime(sales["Delivery Date"])

# Orders with delivery dates
delivered = sales.dropna(subset=["Delivery Date"]).copy()
delivered["Delivery_Days"] = (delivered["Delivery Date"] - delivered["Order Date"]).dt.days

deliv_store = delivered.merge(stores[["StoreKey", "Country"]], on="StoreKey", how="left", suffixes=("", "_store"))
deliv_store["StoreType"] = np.where(deliv_store["StoreKey"] == 0, "Online", "Physical")

avg_del = deliv_store["Delivery_Days"].mean()
med_del = deliv_store["Delivery_Days"].median()
min_del = deliv_store["Delivery_Days"].min()
max_del = deliv_store["Delivery_Days"].max()
delivery_pct = len(delivered) / len(sales) * 100

type_del = deliv_store.groupby("StoreType")["Delivery_Days"].agg(["mean", "median", "count"]).round(1)
country_del = deliv_store.groupby("Country")["Delivery_Days"].agg(["mean", "median", "count"]).round(1)
country_del = country_del[country_del["count"] >= 10].sort_values("mean")

print("DELIVERY & FULFILLMENT")
print(f"  Orders with delivery: {len(delivered):,} / {len(sales):,} ({delivery_pct:.1f}%)")
print(f"  Avg delivery: {avg_del:.1f} days")

# Charts
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].hist(deliv_store["Delivery_Days"], bins=30, color="teal", edgecolor="white")
axes[0].axvline(avg_del, color="red", ls="--", label=f"Avg: {avg_del:.1f} days")
axes[0].axvline(med_del, color="orange", ls="--", label=f"Median: {med_del:.0f} days")
axes[0].set_title("Delivery Time Distribution (days)")
axes[0].legend()

axes[1].bar(type_del.index, type_del["mean"], color=["seagreen", "steelblue"])
axes[1].set_title("Avg Delivery Time: Online vs Physical")
axes[1].set_ylabel("Days")
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "a4_delivery_overview.png"), dpi=100)
plt.close()
print("  Chart: a4_delivery_overview.png")

# Report
lines = []
lines.append("# Delivery & Fulfillment Analysis Report")
lines.append("")
lines.append("## Overview")
lines.append("")
lines.append(f"- **Orders with delivery recorded:** {len(delivered):,} / {len(sales):,} ({delivery_pct:.1f}%)")
lines.append(f"- **Orders without delivery date:** {sales['Delivery Date'].isna().sum():,} (excluded from analysis)")
lines.append("")
lines.append("## Overall Delivery Statistics")
lines.append("")
lines.append("| Metric | Value |")
lines.append("|---|---|")
lines.append(f"| Average Delivery Time | {avg_del:.1f} days |")
lines.append(f"| Median Delivery Time | {med_del:.0f} days |")
lines.append(f"| Fastest Delivery | {min_del} day(s) |")
lines.append(f"| Slowest Delivery | {max_del} days |")
lines.append(f"| Total Delivered Orders | {len(delivered):,} |")

lines.append("")
lines.append("## Delivery Time by Store Type")
lines.append("")
lines.append("| Store Type | Avg (days) | Median (days) | Orders |")
lines.append("|---|---|---|---|")
for t, row in type_del.iterrows():
    lines.append(f"| {t} | {row['mean']:.1f} | {row['median']:.0f} | {row['count']:,} |")

lines.append("")
lines.append("## Fastest Countries (Top 10)")
lines.append("")
lines.append("| Country | Avg (days) | Median (days) | Orders |")
lines.append("|---|---|---|---|")
for c, row in country_del.head(10).iterrows():
    lines.append(f"| {c} | {row['mean']:.1f} | {row['median']:.0f} | {row['count']:,} |")

lines.append("")
lines.append("## Slowest Countries (Bottom 5)")
lines.append("")
lines.append("| Country | Avg (days) | Median (days) | Orders |")
lines.append("|---|---|---|---|")
for c, row in country_del.tail(5).iterrows():
    lines.append(f"| {c} | {row['mean']:.1f} | {row['median']:.0f} | {row['count']:,} |")

lines.append("")
lines.append("## Charts")
lines.append("")
lines.append("- `reports/figures/a4_delivery_overview.png`")
lines.append("")
lines.append("## Key Insights")
lines.append("")
lines.append(f"- Average delivery takes **{avg_del:.1f} days** (median: {med_del:.0f} days)")
if "Online" in type_del.index and "Physical" in type_del.index:
    diff = abs(type_del.loc["Physical", "mean"] - type_del.loc["Online", "mean"])
    faster = "Online" if type_del.loc["Online", "mean"] < type_del.loc["Physical", "mean"] else "Physical"
    lines.append(f"- **{faster}** delivers {diff:.1f} days faster on average")

lines.append("")
lines.append("## Limitations")
lines.append("")
lines.append(f"- Only **{delivery_pct:.1f}%** of orders have delivery dates -- results may be biased")
lines.append("- Delivery time is calendar days, not business days")

with open(os.path.join(BASE, "reports", "delivery-analysis-report.md"), "w") as f:
    f.write("\n".join(lines))
print("  Report: reports/delivery-analysis-report.md")
print("DELIVERY ANALYSIS COMPLETE\n")
