# Data Analytics Projects

This folder contains several analytics projects focused on retail, hospitality, automotive, and sports data. Each project includes source datasets, analysis notebooks, and Power BI reports or dashboards.

## Projects

### 1. Candy Distributor Analysis
- Folder: `Candy_Distributor_Analysis/`
- Description: A comprehensive candy distribution analytics project that includes data preprocessing, data quality checks, feature engineering, exploratory analysis, and Power BI dashboard reporting.
- Key artifacts:
  - `candy_distribution.pbix`
  - `candy_distribution_Dashboard.pdf`
  - `requirements.txt`
  - `data/version_2/candy_data.csv`
  - `division_mismatches.csv`
  - `Candy_Distributor_Analysis_Report.md`
- Notes: Uses Python notebooks and versioned datasets for repeatable data engineering.

### 2. Car Data Analysis
- Folder: `Car Data Analysis/`
- Description: A vehicle analytics project exploring pricing, fuel efficiency, brand comparisons, and market trends.
- Key artifacts:
  - `All_cars_dataset.csv`
  - `All_cars_dataset.pbix`
  - `All_cars_dataset.pdf`
  - `Readme.md`
- Notes: Includes a summary README and visual dashboard outputs.

### 3. Revenue Insights in Hospitality Domain Report
- Folder: `Revenue Insights in Hospitality Domain Report/`
- Description: A hospitality-focused revenue analytics dashboard for hotel bookings, occupancy, revenue, and booking channel performance.
- Key artifacts:
  - `project1.pbip`
  - `Revenue_Insights_hospitality_Domain.ipynb`
  - `Revenue Insights Hospitality Domain Data Analytics Report.pdf`
  - `data/` with hotel, room, booking, and date dimension datasets
- Notes: Contains a README that explains the dashboard and visualizations.

### 4. T20 Cricket Analytics Report
- Folder: `T20 CRICKET ANALYTICS REPORT/`
- Description: A sports analytics dashboard centered on T20 cricket performance metrics for batting, bowling, teams, and match trends.
- Key artifacts:
  - `T20 CRICKET ANALYTICS.pbix`
  - `T20 CRICKET ANALYTICS.pdf`
  - `Readme.md`
  - `dim_*` and `fact_*` CSV datasets
- Notes: Supports interactive Power BI reporting and player/team performance insights.

## How to Use

1. Open the relevant project folder.
2. Review the project README or report note for details on the dataset and analysis goals.
3. Run the notebooks in the folder using Jupyter Notebook or Jupyter Lab.
4. Open Power BI files (`.pbix` / `.pbip`) with Power BI Desktop for interactive dashboards.

## Technical Notes
- The `Candy_Distributor_Analysis` project includes a Python dependency manifest at `requirements.txt`.
- Many projects contain export-ready PDF reports for quick review.
- Datasets are stored alongside notebooks and dashboard files to preserve reproducibility.

## Recommended Next Steps
- Add a top-level project README for each folder that lacks one.
- Standardize folder names to avoid spaces if you plan to use scripts or automation.
- Include a `requirements.txt` or `environment.yml` per Python-based project.
- Add a summary of business questions and key findings for each project.
