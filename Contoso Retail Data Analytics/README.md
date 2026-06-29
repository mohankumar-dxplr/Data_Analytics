# Contoso Retail Data Analytics

## Project Overview

This project analyzes retail sales data from **Contoso** -- a multi-brand electronics and home goods retailer with physical stores across 8 countries and an online channel. The dataset spans **2016--2021** with 62,884 sales transactions, 15,266 customers, 2,517 products, and 67 stores.

## Repository Structure

```
sample/
|-- data/
|   |-- raw/               # Original, unmodified source CSV files (6 files)
|   |-- cleaned/           # Cleaned and standardized data (ready for analysis)
|   |-- transformed/       # Aggregated / enriched datasets (6 CSV files)
|-- notebooks/            # Jupyter notebooks (executed with .venv)
|   |-- analysis/          # 7 notebooks (a1-a6 + run_all)
|   |-- data/              # 2 notebooks (clean_data, transform_data)
|   |-- eda/               # 3 notebooks (explore, storekey, eda)
|-- scripts/
|   |-- data/              # Data pipeline scripts
|   |   |-- clean_data.py         # Clean raw data --> cleaned/
|   |   |-- transform_data.py     # Transform cleaned data --> transformed/
|   |-- eda/               # Exploratory Data Analysis scripts
|   |   |-- explore_raw_data.py   # Initial raw data assessment
|   |   |-- investigate_storekey.py  # Deep dive into StoreKey = 0 (Online)
|   |   |-- eda_cleaned_data.py      # Full EDA on cleaned data (10 charts)
|   |-- analysis/          # Analysis scripts (6 core + runner + utility)
|   |   |-- a1_revenue_analysis.py         # Revenue, profit, margin
|   |   |-- a2_customer_segmentation.py    # RFM segmentation
|   |   |-- a3_time_series.py              # Monthly/yearly/quarterly trends
|   |   |-- a4_delivery_analysis.py        # Delivery time & fulfillment
|   |   |-- a5_product_affinity.py         # Cross-sell product pairs
|   |   |-- a6_executive_dashboard.py      # KPI summary chart + report
|   |   |-- run_all.py                     # Master runner (all 6 in sequence)
|   |   |-- fix_encoding.py                # Utility: replace non-ASCII chars
|   |-- build_client_report.py      # Builds both copies of client executive report
|   |-- check_report_quality.py     # Validates report file integrity
|-- reports/
|   |-- figures/           # All generated charts (PNG) -- 23 total
|   |-- CLIENT-EXECUTIVE-REPORT.md # Client report copy (for viewing inside reports/)
|   |-- data cleaning report.md
|   |-- data transformation report.md
|   |-- understanding-data report.md
|   |-- revenue-analysis-report.md
|   |-- customer-segmentation-report.md
|   |-- time-series-report.md
|   |-- delivery-analysis-report.md
|   |-- product-affinity-report.md
|   |-- executive-dashboard-report.md
|   |-- covid-recovery-investigation.md
|   |-- executive-consolidated-report.md
|-- .opencode/
|   |-- skills/            # AI agent skill definitions for assisted analysis
|-- .venv/                 # Python virtual environment (Python 3.12)
|-- requirements.txt       # Python dependencies
|-- AGENTS.md              # AI agent behavior guidelines
|-- CLIENT-EXECUTIVE-REPORT.md             # Client-facing executive report (root view)
|-- README.md              # This file
```

## Pipeline Stages

| Stage | Description | Input | Output |
|---|---|---|---|
| **1. Raw Data** | Original source exports | -- | `data/raw/` |
| **2. Data Cleaning** | Fix encoding, convert types, handle missing values | `data/raw/` | `data/cleaned/` |
| **3. EDA** | Understand distributions, relationships, patterns | `data/cleaned/` | `reports/figures/` |
| **4. Transformation** | Enrich data, aggregate | `data/cleaned/` | `data/transformed/` |
| **5. Core Analysis** | 6 workstreams (revenue, RFM, trends, delivery, affinity, dashboard) | `data/cleaned/` | `reports/` + `figures/` |
| **6. Investigation** | Deep-dive into COVID-19 impact & recovery | `data/cleaned/` | `covid-recovery-investigation.md` |
| **7. Client Reporting** | Build client-friendly executive report | All analysis | `CLIENT-EXECUTIVE-REPORT.md` + `reports/CLIENT-EXECUTIVE-REPORT.md` |
| **8. Integrity Check** | Validate reports for empty cells, encoding, paths | Report files | Validation summary |

## Running the Scripts

All scripts use absolute paths -- run them from the repository root:

```powershell
# Activate virtual environment (required)
.\.venv\Scripts\Activate

# Data pipeline
python scripts/data/clean_data.py
python scripts/data/transform_data.py

# Exploratory analysis
python scripts/eda/explore_raw_data.py
python scripts/eda/investigate_storekey.py
python scripts/eda/eda_cleaned_data.py

# All 6 core analyses (recommended)
python scripts/analysis/run_all.py

# Or run individually:
python scripts/analysis/a1_revenue_analysis.py
python scripts/analysis/a2_customer_segmentation.py
python scripts/analysis/a3_time_series.py
python scripts/analysis/a4_delivery_analysis.py
python scripts/analysis/a5_product_affinity.py
python scripts/analysis/a6_executive_dashboard.py

# Build client executive report (after all analyses are complete)
python scripts/build_client_report.py

# Validate report integrity
python scripts/check_report_quality.py
```

## Running the Notebooks

Notebooks in `notebooks/` have been pre-executed with the `.venv` environment and contain all outputs. To launch the Jupyter interface or re-execute:

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate

# Launch Jupyter notebook server
jupyter-notebook notebooks/

# Or re-execute from command line (overwrites outputs):
python -m jupyter nbconvert --to notebook --execute notebooks/analysis/a1_revenue_analysis.ipynb --inplace
```

**Notebooks (12 total, organized by subdirectory):**

| Notebook | Description |
|---|---|
| `data/clean_data.ipynb` | Data cleaning pipeline |
| `data/transform_data.ipynb` | Data transformation & enrichment |
| `eda/explore_raw_data.ipynb` | Raw data assessment |
| `eda/investigate_storekey.ipynb` | Online store (StoreKey=0) deep-dive |
| `eda/eda_cleaned_data.ipynb` | Full EDA with 10 charts |
| `analysis/a1_revenue_analysis.ipynb` | Revenue, profit, margin by category/country |
| `analysis/a2_customer_segmentation.ipynb` | RFM segmentation (Champions/Loyal/Potential/At Risk/Lost) |
| `analysis/a3_time_series.ipynb` | Monthly/yearly/quarterly trends with corrected growth |
| `analysis/a4_delivery_analysis.ipynb` | Delivery time statistics (4.5 days avg) |
| `analysis/a5_product_affinity.ipynb` | Cross-sell: 67,894 product pairs identified |
| `analysis/a6_executive_dashboard.ipynb` | KPI summary with 6-panel dashboard chart |
| `analysis/run_all.ipynb` | Master runner executing all 6 in sequence |

## Key Findings

### Business Overview
- **Total Revenue:** $55.8M across 26,326 orders and 197,757 units
- **Total Profit:** $32.7M (58.6% margin)
- **Customers:** 15,266 across 8 countries, balanced gender split (~50/50)
- **Online share:** ~21% of revenue

### Pre-COVID Growth (2016-2019)
- Revenue grew **+163%** from $6.9M to **$18.3M** (peak in Dec 2019)
- **Computers** category drove **48%** of all growth ($1.5M --> $7.0M, +265%)
- Cell Phones (+16.6%) and Cameras (+11.6%) contributed significantly

### COVID-19 Impact
- Revenue declined **-49.1%** from 2019 ($18.3M) to 2020 ($9.3M)
- Crash was severe: Feb 2020 ($2.2M) --> Apr 2020 trough (**$218K**, -90%)
- **82% customer churn** -- only 2,075 of 11,323 pre-COVID customers returned
- Even retained customers cut spending by -48%
- **No meaningful recovery** observed within data period (through Feb 2021)

### Margins & Resilience
- Profit margins stayed stable at ~58% across ALL categories (+/- 1pp)
- Business did not resort to discounting during the crisis

### Delivery & Operations
- 20.9% of orders have recorded delivery dates (data quality gap)
- Average delivery: 4.5 days (online slightly faster)
- 65.1% of orders contain multiple items -- 67,894 unique product pairs identified

### Customer Segmentation (RFM)
- **Champions** (highest value): buy recently, often, spend most -- reward & nurture
- **Loyal**: regular customers, good spend -- upsell & cross-sell
- **Potential**: moderate engagement -- grow relationship
- **At Risk**: used to buy but haven't recently -- re-engage campaigns
- **Lost**: long dormant -- win-back or ignore

## Reports Generated

| Priority | Report | Description |
|---|---|---|
| **FOR CLIENTS** 🎯 | `CLIENT-EXECUTIVE-REPORT.md` | **Client-facing report** with all 23 charts, insights, and recommendations (root level, images show everywhere) |
| **FOR CLIENTS** 🎯 | `reports/CLIENT-EXECUTIVE-REPORT.md` | Same report — alternate copy for viewing inside `reports/` folder |
| **START HERE** | `executive-consolidated-report.md` | **Master technical summary** combining all findings + recommendations |
| Core | `revenue-analysis-report.md` | Revenue, profit, margin by category, country, store type |
| Core | `customer-segmentation-report.md` | RFM analysis with 5 segments |
| Core | `time-series-report.md` | Monthly/yearly/quarterly trends with corrected growth |
| Core | `delivery-analysis-report.md` | Delivery time statistics by store type and country |
| Core | `product-affinity-report.md` | Top product & category pairs bought together |
| Core | `executive-dashboard-report.md` | KPI summary with 6-panel chart |
| Investigation | `covid-recovery-investigation.md` | Deep-dive: category/country/customer COVID impact |
| Pipeline | `data cleaning report.md` | Data cleaning steps and decisions |
| Pipeline | `data transformation report.md` | Data transformation documentation |
| Pipeline | `understanding-data report.md` | Initial data exploration findings |

### Charts (`reports/figures/`) -- 23 total PNGs

**EDA (10 charts):** age/gender, top states, category price, cost vs price, stores map, sales overview, exchange rates, cross-category gender, top subcategories, age group sales

**Core Analysis (8 charts):** revenue overview, margin by category, customer segments, top customers, time series, delivery overview, product affinity, executive dashboard

**Investigation (5 charts):** COVID trend, category recovery, country heatmap, customer churn waterfall, online vs physical

> 💡 **All 23 charts** are embedded with figure references in the **[Client Executive Report](CLIENT-EXECUTIVE-REPORT.md)** (see Section 12 — Visual Index for the complete gallery).

## Dependencies

See `requirements.txt`. Core libraries: pandas, numpy, matplotlib, seaborn, plotly, scikit-learn.
