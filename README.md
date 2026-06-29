# Data Analytics Projects

A monorepo of end-to-end data analytics projects spanning retail, hospitality, automotive, and sports domains. Each project follows the full analytics lifecycle — data ingestion, cleaning, transformation, exploratory analysis, feature engineering, visualization, and interactive Power BI dashboard reporting.

---

## Projects

### 1. Contoso Retail Data Analytics
- Folder: `Contoso Retail Data Analytics/`
- Description: Mature retail analytics pipeline for a global retailer. Includes a formal data pipeline (raw → cleaned → transformed), RFM customer segmentation, revenue/profit analysis, time-series trends, delivery/fulfillment analysis, product affinity mining, and a client-facing executive report with 23 embedded charts.
- Key artifacts:
  - `scripts/data/clean_data.py` and `transform_data.py` — data pipeline
  - `scripts/analysis/a1`–`a6` — 6 analysis workstreams
  - `scripts/analysis/run_all.py` — master runner
  - `CLIENT-EXECUTIVE-REPORT.md` — 658-line client-facing report
  - `reports/` — 11 detailed markdown reports + 23 PNG charts
  - `data/raw/`, `data/cleaned/`, `data/transformed/` — versioned datasets
- Key findings: $55.8M revenue, 58.6% profit margin, +163% pre-COVID growth, −49.1% COVID decline, 5 RFM customer segments, 67K+ product affinity pairs.
- Technologies: Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, scikit-learn

### 2. Candy Distributor Analysis
- Folder: `Candy_Distributor_Analysis/`
- Description: Comprehensive candy supply chain analytics covering data preprocessing, data quality checks (division mismatches), feature engineering, exploratory analysis, and interactive Power BI dashboarding. Uses versioned datasets for reproducible data engineering.
- Key artifacts:
  - `candy_distribution.pbix` and `candy_distribution_Dashboard.pdf`
  - `candy_data.csv` — final consolidated dataset (10,189 rows)
  - `division_mismatches.csv` — data quality output
  - `data/version_0/`, `version_1/`, `version_2/` — versioned data
  - `data_preprocessing/` — 5 cleaning notebooks
  - `feature_engineering/` — 3 notebooks for derived features
  - `visuals/` — 7 visualization notebooks + `pivottablejs.html`
  - `requirements.txt` — 54 pinned Python packages
- Technologies: Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, scikit-learn, pygwalker, edvart, pivottablejs

### 3. Revenue Insights in Hospitality Domain
- Folder: `Revenue Insights in Hospitality Domain Report/`
- Description: Hospitality revenue analytics dashboard analyzing hotel bookings, occupancy rates, revenue by category (Luxury/Business), booking platform performance, and weekly trends across 4 cities.
- Key artifacts:
  - `project1.pbip` — Power BI project (modern format)
  - `Revenue_Insights_hospitality_Domain.ipynb` — full analysis notebook (~1,185 lines)
  - `Revenue Insights Hospitality Domain Data Analytics Report.pdf`
  - `data/dim_hotels.csv` — 26 hotels, `fact_bookings.csv` — 134,591 booking records
  - `project1.SemanticModel/model.bim` — tabular semantic model
- Technologies: Python, Pandas, Power BI, DAX

### 4. T20 Cricket Analytics Report
- Folder: `T20 CRICKET ANALYTICS REPORT/`
- Description: Sports analytics dashboard for T20 cricket covering batting/bowling performance metrics, team comparisons, match summaries, and player profiling across 46 matches and 230 players.
- Key artifacts:
  - `T20 CRICKET ANALYTICS.pbix` and `T20 CRICKET ANALYTICS.pdf`
  - `dim_match_summary.csv` — 46 matches, `dim_players.csv` — 230 players
  - `fact_bating_summary.csv` — 700 batting records
  - `fact_bowling_summary.csv` — 501 bowling records
- Technologies: Power BI, DAX

### 5. Car Data Analysis
- Folder: `Car Data Analysis/`
- Description: Automotive analytics project exploring vehicle pricing, fuel efficiency, engine specifications, brand comparisons, and market trends across 151 car models.
- Key artifacts:
  - `All_cars_dataset.csv` — 151 entries, 22 columns (Price, Mileage, ENGINE, TRANSMISSION, FUEL TYPE, etc.)
  - `All_cars_dataset.pbix` and `All_cars_dataset.pdf`
- Technologies: Power BI, DAX

---

## Repository Structure

```
Data_Analytics/
├── Contoso Retail Data Analytics/     # Retail — most mature, formal pipeline + client report
├── Candy_Distributor_Analysis/        # Supply chain — versioned data, feature engineering
├── Revenue Insights in Hospitality/   # Hospitality — 134K booking records, Power BI project
├── T20 CRICKET ANALYTICS REPORT/      # Sports — batting/bowling/match analytics
└── Car Data Analysis/                 # Automotive — car specs & pricing dashboard
```

---

## How to Use

1. Navigate into any project folder and review its `README.md` for project-specific details.
2. **Python analysis**: Run `.ipynb` notebooks in Jupyter Lab/Notebook or execute `.py` scripts directly.
3. **Power BI dashboards**: Open `.pbix` or `.pbip` files with Power BI Desktop.
4. **PDF reports**: Quick-scan exported dashboards and reports in `.pdf` format.

---

## Technical Notes

- **Python version**: 3.x recommended across all projects.
- **Dependencies**: `Candy_Distributor_Analysis/requirements.txt` (54 pinned packages) and `Contoso Retail Data Analytics/requirements.txt` (6 unpinned packages) are available.
- **Power BI**: `.pbix` files require Power BI Desktop; `.pbip` is the modern Power BI project format.
- **Data versioning**: The Candy project uses a `version_0` → `version_1` → `version_2` pipeline for reproducibility.
- **Total artifacts**: ~44 scripts/notebooks, ~35+ CSV datasets, 4 Power BI dashboards, 4 PDF exports, 25+ PNG visuals, 15+ markdown reports.

---

## Technologies Used

| Technology | Usage |
|---|---|
| Python | Primary analysis language across all projects |
| Pandas / NumPy | Data manipulation and numerical operations |
| Matplotlib / Seaborn | Static and statistical visualizations |
| Plotly | Interactive visualizations |
| scikit-learn | RFM segmentation, preprocessing |
| Power BI + DAX | Interactive dashboards and reporting |
| Jupyter Notebook | Interactive development environment |
| pygwalker / edvart | Exploratory GUI and automated profiling (Candy) |
