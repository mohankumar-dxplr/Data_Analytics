"""
Master Runner: Executes all 6 analyses in sequence
"""
import sys
import os
from datetime import datetime

BASE = r"C:\Users\Mohan\Downloads\sample"
SCRIPTS_DIR = os.path.join(BASE, "scripts", "analysis")

analyses = [
    ("1. Revenue Analysis", "a1_revenue_analysis.py"),
    ("2. Customer Segmentation", "a2_customer_segmentation.py"),
    ("3. Time Series / Trends", "a3_time_series.py"),
    ("4. Delivery & Fulfillment", "a4_delivery_analysis.py"),
    ("5. Product Affinity", "a5_product_affinity.py"),
    ("6. Executive Dashboard", "a6_executive_dashboard.py"),
]

print("=" * 70)
print("  RUNNING ALL 6 ANALYSES")
print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

for name, script in analyses:
    script_path = os.path.join(SCRIPTS_DIR, script)
    print(f"\n{'=' * 50}")
    print(f"  [{name}]")
    print(f"{'=' * 50}")
    
    ret = os.system(f'python "{script_path}"')
    
    if ret != 0:
        print(f"  ERROR: {name} failed with code {ret}")
        sys.exit(1)

print("\n" + "=" * 70)
print("  ALL 6 ANALYSES COMPLETED SUCCESSFULLY")
print(f"  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

print("\nGenerated files:")
REPORT_DIR = os.path.join(BASE, "reports")
FIGURE_DIR = os.path.join(REPORT_DIR, "figures")

for f in sorted(os.listdir(REPORT_DIR)):
    if f.endswith(".md") and f != "README.md":
        print(f"  reports/{f}")
for f in sorted(os.listdir(FIGURE_DIR)):
    if f.startswith("a") and f.endswith(".png"):
        print(f"  reports/figures/{f}")
