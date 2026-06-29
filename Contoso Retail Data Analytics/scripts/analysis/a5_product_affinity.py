"""
Analysis 5: Product Affinity
Generates reports/product-affinity-report.md + charts
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from itertools import combinations

BASE = r"C:\Users\Mohan\Downloads\sample"
CLEAN_DIR = os.path.join(BASE, "data", "cleaned")
FIGURE_DIR = os.path.join(BASE, "reports", "figures")
os.makedirs(FIGURE_DIR, exist_ok=True)
sns.set_style("whitegrid")

sales = pd.read_csv(os.path.join(CLEAN_DIR, "Sales.csv"))
prod = pd.read_csv(os.path.join(CLEAN_DIR, "Products.csv"))

# Orders with multiple items
multi_item = sales.groupby("Order Number").filter(lambda x: len(x) > 1)
n_multi_orders = multi_item["Order Number"].nunique()
n_total_orders = sales["Order Number"].nunique()
multi_pct = n_multi_orders / n_total_orders * 100

print("PRODUCT AFFINITY")
print(f"  Multi-item orders: {n_multi_orders:,} / {n_total_orders:,} ({multi_pct:.1f}%)")

# Generate product pairs
order_products = sales.groupby("Order Number")["ProductKey"].apply(list).reset_index()
order_products["Count"] = order_products["ProductKey"].apply(len)
multi_orders = order_products[order_products["Count"] >= 2].copy()

pairs = []
for _, row in multi_orders.iterrows():
    prods = sorted(row["ProductKey"])
    for pair in combinations(prods, 2):
        pairs.append(pair)

pairs_df = pd.DataFrame(pairs, columns=["Product_A", "Product_B"])
pair_counts = pairs_df.groupby(["Product_A", "Product_B"]).size().reset_index(name="Frequency")
pair_counts = pair_counts.sort_values("Frequency", ascending=False)

print(f"  Unique product pairs: {len(pair_counts):,}")

# Top pairs with names
top_pairs = pair_counts.head(15).copy()
top_pairs = top_pairs.merge(prod[["ProductKey", "Product Name"]], left_on="Product_A", right_on="ProductKey", how="left")
top_pairs = top_pairs.merge(prod[["ProductKey", "Product Name"]], left_on="Product_B", right_on="ProductKey", how="left", suffixes=("_A", "_B"))
top_pairs = top_pairs.drop(columns=["ProductKey_A", "ProductKey_B"])

# Category-level affinity
sales_cat = sales.merge(prod[["ProductKey", "Category"]], on="ProductKey", how="left")
multi_cat = sales_cat[sales_cat["Order Number"].isin(multi_item["Order Number"].unique())]
order_cats = multi_cat.groupby("Order Number")["Category"].apply(lambda x: sorted(set(x))).reset_index()
multi_cat_orders = order_cats[order_cats["Category"].apply(len) >= 2].copy()

cat_pairs = []
for _, row in multi_cat_orders.iterrows():
    cats = row["Category"]
    for pair in combinations(cats, 2):
        cat_pairs.append(tuple(sorted(pair)))

cat_pair_counts = pd.DataFrame(cat_pairs, columns=["Cat_A", "Cat_B"])
cat_pair_counts = cat_pair_counts.groupby(["Cat_A", "Cat_B"]).size().reset_index(name="Frequency")
cat_pair_counts = cat_pair_counts.sort_values("Frequency", ascending=False).head(10)

# Chart
fig, ax = plt.subplots(figsize=(10, 6))
labels = [f"{row['Product Name_A'][:25]} + {row['Product Name_B'][:25]}" for _, row in top_pairs.head(10).iterrows()]
ax.barh(labels[::-1], top_pairs.head(10)["Frequency"].iloc[::-1], color="steelblue")
ax.set_title("Top 10 Product Pairs Bought Together")
ax.set_xlabel("Number of Orders")
plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "a5_product_affinity.png"), dpi=100)
plt.close()
print("  Chart: a5_product_affinity.png")

# Report
lines = []
lines.append("# Product Affinity Analysis Report")
lines.append("")
lines.append("## Overview")
lines.append("")
lines.append(f"- **Total Orders:** {n_total_orders:,}")
lines.append(f"- **Orders with multiple items:** {n_multi_orders:,} ({multi_pct:.1f}%)")
lines.append(f"- **Unique product pairs found:** {len(pair_counts):,}")
lines.append("")
lines.append("## Top 10 Product Pairs")
lines.append("")
lines.append("| Product A | Product B | Times Bought Together |")
lines.append("|---|---|---|")
for _, row in top_pairs.head(10).iterrows():
    lines.append(f"| {row['Product Name_A']} | {row['Product Name_B']} | {row['Frequency']:,} |")

lines.append("")
lines.append("## Top Category Pairs")
lines.append("")
lines.append("| Category A | Category B | Frequency |")
lines.append("|---|---|---|")
for _, row in cat_pair_counts.iterrows():
    lines.append(f"| {row['Cat_A']} | {row['Cat_B']} | {row['Frequency']:,} |")

lines.append("")
lines.append("## Charts")
lines.append("")
lines.append("- `reports/figures/a5_product_affinity.png`")
lines.append("")
lines.append("## Key Insights")
lines.append("")
lines.append(f"- {len(pair_counts):,} unique product pairs across {n_multi_orders:,} multi-item orders")
lines.append(f"- Top pair: **{top_pairs.iloc[0]['Product Name_A']}** + **{top_pairs.iloc[0]['Product Name_B']}** ({top_pairs.iloc[0]['Frequency']:,} orders)")
lines.append(f"- **{multi_pct:.1f}%** of orders contain multiple items (cross-sell opportunity)")

lines.append("")
lines.append("## Limitations")
lines.append("")
lines.append("- Only pairwise combinations considered (not 3+ product bundles)")
lines.append("- Does not account for product popularity baseline (no lift score)")

with open(os.path.join(BASE, "reports", "product-affinity-report.md"), "w") as f:
    f.write("\n".join(lines))
print("  Report: reports/product-affinity-report.md")
print("PRODUCT AFFINITY COMPLETE\n")
