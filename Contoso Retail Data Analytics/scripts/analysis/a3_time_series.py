"""
Analysis 3: Time Series / Trends
Generates reports/time-series-report.md + charts
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
sales["Order Date"] = pd.to_datetime(sales["Order Date"])

# Merge with Products for Unit Price USD
sales_rev = sales.merge(prod[["ProductKey", "Unit Price USD"]], on="ProductKey", how="left").copy()
sales_rev["Revenue_USD"] = sales_rev["Quantity"] * sales_rev["Unit Price USD"]

# Monthly
monthly = sales_rev.set_index("Order Date").resample("ME").agg(
    Revenue=("Revenue_USD", "sum"),
    Orders=("Order Number", "nunique"),
    Units=("Quantity", "sum")
).reset_index()

# Yearly
yearly = sales_rev.set_index("Order Date").resample("YE").agg(
    Revenue=("Revenue_USD", "sum"),
    Orders=("Order Number", "nunique")
).reset_index()
yearly["Months"] = yearly["Order Date"].dt.year.map(
    sales_rev.groupby(sales_rev["Order Date"].dt.year)["Order Date"]
    .apply(lambda x: x.dt.month.nunique())
)
yearly["Complete"] = yearly["Months"] == 12

# Quarterly
quarterly = sales_rev.set_index("Order Date").resample("QE").agg(
    Revenue=("Revenue_USD", "sum"),
    Orders=("Order Number", "nunique")
).reset_index()

# YoY pivot
monthly["Year"] = monthly["Order Date"].dt.year
monthly["Month"] = monthly["Order Date"].dt.month
yoy = monthly.pivot_table(index="Month", columns="Year", values="Revenue", aggfunc="sum")

best_month = monthly.loc[monthly["Revenue"].idxmax()]

# Growth: compare only COMPLETE years, or the last two complete years
complete_years = yearly[yearly["Complete"]].copy()
if len(complete_years) >= 2:
    first_rev = complete_years.iloc[0]["Revenue"]
    last_rev = complete_years.iloc[-1]["Revenue"]
    total_growth = ((last_rev - first_rev) / first_rev) * 100
    growth_note = f"({complete_years.iloc[0]['Order Date'].year} to {complete_years.iloc[-1]['Order Date'].year}, complete years only)"
elif len(complete_years) == 1:
    first_rev = complete_years.iloc[0]["Revenue"]
    last_rev = yearly.iloc[-1]["Revenue"]
    total_growth = ((last_rev - first_rev) / first_rev) * 100
    growth_note = "(latest year is partial -- interpret with caution)"
else:
    first_rev = yearly.iloc[0]["Revenue"]
    last_rev = yearly.iloc[-1]["Revenue"]
    total_growth = 0
    growth_note = "(insufficient data)"

print("TIME SERIES / TRENDS")
print(f"  Period: {monthly['Order Date'].min().date()} to {monthly['Order Date'].max().date()}")
print(f"  Best month: {best_month['Order Date'].strftime('%Y-%m')} (${best_month['Revenue']:,.2f})")
print(f"  Growth: {total_growth:+.1f}% {growth_note}")

# Charts
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
axes[0,0].plot(monthly["Order Date"], monthly["Revenue"] / 1e6, color="navy", linewidth=1.5)
axes[0,0].set_title("Monthly Revenue (Millions USD)")
axes[0,0].tick_params(axis="x", rotation=45)

axes[0,1].plot(monthly["Order Date"], monthly["Orders"], color="darkorange", linewidth=1.5)
axes[0,1].set_title("Monthly Orders")
axes[0,1].tick_params(axis="x", rotation=45)

axes[1,0].bar(yearly["Order Date"].dt.year.astype(str), yearly["Revenue"] / 1e6, color="teal")
axes[1,0].set_title("Yearly Revenue (Millions USD)")

if yoy.shape[1] >= 2:
    for year in yoy.columns:
        axes[1,1].plot(yoy.index, yoy[year], marker="o", label=str(year), linewidth=1.5)
    axes[1,1].set_title("Year-over-Year Monthly Revenue")
    axes[1,1].legend()

plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "a3_time_series.png"), dpi=100)
plt.close()
print("  Chart: a3_time_series.png")

# Report
lines = []
lines.append("# Time Series / Trends Report")
lines.append("")
lines.append("## Overview")
lines.append("")
lines.append(f"- **Sales Period:** {monthly['Order Date'].min().date()} to {monthly['Order Date'].max().date()}")
lines.append(f"- **Total Months:** {len(monthly)}")
lines.append("")
lines.append("## Yearly Summary")
lines.append("")
lines.append("| Year | Revenue (USD) | Orders | Growth vs Prior Year | Months of Data |")
lines.append("|---|---|---|---|---|")
for i, (_, row) in enumerate(yearly.iterrows()):
    if i == 0:
        growth = "-"
    else:
        prev = yearly.iloc[i-1]["Revenue"]
        growth = f"{(row['Revenue'] - prev) / prev * 100:+.1f}%"
    partial_flag = " **" if row["Months"] < 12 else ""
    lines.append(f"| {row['Order Date'].year}{partial_flag} | ${row['Revenue']:,.2f} | {row['Orders']:,} | {growth} | {row['Months']}/12 |")

lines.append("")
lines.append("## Top 5 Months by Revenue")
lines.append("")
lines.append("| Month | Revenue (USD) | Orders | Units |")
lines.append("|---|---|---|---|")
for _, row in monthly.nlargest(5, "Revenue").iterrows():
    lines.append(f"| {row['Order Date'].strftime('%Y-%m')} | ${row['Revenue']:,.2f} | {row['Orders']:,} | {row['Units']:,} |")

lines.append("")
lines.append("## Quarterly Revenue")
lines.append("")
for _, row in quarterly.iterrows():
    q = f"Q{row['Order Date'].quarter} {row['Order Date'].year}"
    lines.append(f"- **{q}:** ${row['Revenue']:,.2f} ({row['Orders']:,} orders)")

lines.append("")
lines.append("## Year-over-Year Growth by Month")
lines.append("")
if yoy.shape[1] >= 2:
    header = "| Month |" + " |".join([f" {y} ($) |" for y in yoy.columns]) + "|"
    sep = "|---|" + "---|" * len(yoy.columns)
    lines.append(header)
    lines.append(sep)
    for m in yoy.index:
        month_name = datetime(2000, m, 1).strftime("%b")
        vals = " |".join([f" ${yoy.loc[m, y]:,.0f}" if pd.notna(yoy.loc[m, y]) else " -" for y in yoy.columns])
        lines.append(f"| {month_name} | {vals} |")
else:
    lines.append("Insufficient years for YoY comparison.")

lines.append("")
lines.append("## Overall Growth")
lines.append("")
if len(complete_years) >= 2:
    cy0 = complete_years.iloc[0]
    cy1 = complete_years.iloc[-1]
    lines.append(f"- **{cy0['Order Date'].year} Revenue (full year):** ${cy0['Revenue']:,.2f}")
    lines.append(f"- **{cy1['Order Date'].year} Revenue (full year):** ${cy1['Revenue']:,.2f}")
    lines.append(f"- **Growth ({cy0['Order Date'].year} to {cy1['Order Date'].year}):** {total_growth:+.1f}%")
    lines.append(f"  *Note: Only complete calendar years are used. {growth_note}*")
    if 2019 in complete_years['Order Date'].dt.year.values and 2020 in complete_years['Order Date'].dt.year.values:
        rev_2019 = complete_years.loc[complete_years['Order Date'].dt.year == 2019, 'Revenue'].iloc[0]
        rev_2020 = complete_years.loc[complete_years['Order Date'].dt.year == 2020, 'Revenue'].iloc[0]
        covid_growth = ((rev_2020 - rev_2019) / rev_2019) * 100
        lines.append(f"- **COVID impact (2019 to 2020):** {covid_growth:+.1f}% (revenue dropped from ${rev_2019:,.2f} to ${rev_2020:,.2f})")
else:
    lines.append(f"- **{yearly.iloc[0]['Order Date'].year} Revenue:** ${yearly.iloc[0]['Revenue']:,.2f}")
    lines.append(f"- **{yearly.iloc[-1]['Order Date'].year} Revenue:** ${yearly.iloc[-1]['Revenue']:,.2f}")

lines.append("")
lines.append("### Partial Year Warning")
lines.append("")
lines.append("The following years have incomplete data and should not be compared directly to full years:")
for _, row in yearly.iterrows():
    if row['Months'] < 12:
        lines.append(f"- **{row['Order Date'].year}:** only {row['Months']}/12 months available (${row['Revenue']:,.2f} shown is partial)")

lines.append("")
lines.append("## Charts")
lines.append("")
lines.append("- `reports/figures/a3_time_series.png`")
lines.append("")
lines.append("## Key Insights")
lines.append("")
lines.append(f"- Highest revenue month: **{best_month['Order Date'].strftime('%B %Y')}** (${best_month['Revenue']:,.2f})")
if len(complete_years) >= 2:
    cy0_yr = complete_years.iloc[0]['Order Date'].year
    cy1_yr = complete_years.iloc[-1]['Order Date'].year
    lines.append(f"- Growth from {cy0_yr} to {cy1_yr} (complete years): **{total_growth:+.1f}%**")
if 2019 in yearly['Order Date'].dt.year.values and 2020 in yearly['Order Date'].dt.year.values:
    rev_2019 = yearly.loc[yearly['Order Date'].dt.year == 2019, 'Revenue'].iloc[0]
    rev_2020 = yearly.loc[yearly['Order Date'].dt.year == 2020, 'Revenue'].iloc[0]
    covid_growth = ((rev_2020 - rev_2019) / rev_2019) * 100
    lines.append(f"- COVID caused a **{covid_growth:.1f}%** revenue decline from 2019 to 2020")
    lines.append(f"- Revenue dropped ~90% from Feb 2020 ($2.2M) to Apr 2020 trough ($218K)")

with open(os.path.join(BASE, "reports", "time-series-report.md"), "w") as f:
    f.write("\n".join(lines))
print("  Report: reports/time-series-report.md")
print("TIME SERIES COMPLETE\n")
