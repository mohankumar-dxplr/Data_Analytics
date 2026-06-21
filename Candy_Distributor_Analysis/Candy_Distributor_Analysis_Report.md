# Candy Distributor Analysis Project Report

## Project Overview

This project is a comprehensive analytics solution for a candy distribution business. It covers data acquisition, preprocessing, data quality validation, feature engineering, exploratory analysis, and dashboard reporting using Power BI and Python.

## Core Deliverables

- `candy_distribution.pbix` - Power BI dashboard file
- `candy_distribution_Dashboard.pdf` - exported dashboard report
- `requirements.txt` - Python environment dependencies
- `candy_data.csv` - consolidated cleaned dataset from preprocessing
- `division_mismatches.csv` - validation output for mismatched division records
- `data/` - raw and versioned source datasets
- `data_preprocessing/` - notebooks for dataset cleaning and preparation
- `feature_engineering/` - notebooks for generating derived features
- `visuals/` - notebooks, charts, and interactive visual outputs

## Data Assets

### Versioned datasets

- `data/version_0/`
  - `Candy_Factories.csv`
  - `Candy_Products.csv`
  - `Candy_Sales.csv`
  - `Candy_Targets.csv`
  - `zips.csv`
  - `candy_distributor_data_dictionary.csv`
  - `data.csv`
- `data/version_1/`
  - clean copies of the factory, product, sales, target, and zip datasets
- `data/version_2/`
  - `candy_data.csv` - final merged dataset ready for analytics

### Data dictionary fields

#### Sales table
- Row ID: Unique row identifier
- Order ID: Unique order identifier
- Order Date: Date of order
- Ship Date: Date of shipment
- Ship Mode: Shipping method
- Customer ID: Unique customer identifier
- Country/Region, City, State/Province, Postal Code
- Division, Region
- Product ID, Product Name
- Sales, Units, Gross Profit, Cost

#### Factories table
- Factory, Latitude, Longitude

#### Products table
- Division, Product Name, Factory, Product ID, Unit Price, Unit Cost

#### Targets table
- Division, Target (Sales Target 2024)

#### US Zips table
- Zip code, latitude, longitude, city, state abbreviation, state name
- ZCTA metadata, population, density, county FIPS and county name
- Military, timezone, and imprecision flags

## Analysis Workflow

### Preprocessing

- `joins.ipynb` merges product, factory, sales, and target data into a consolidated dataset.
- Data quality checks were performed for division mismatches between product and target tables.
- Mismatched records were identified and exported to `division_mismatches.csv`.
- Rows with known issues were removed and the final cleaned dataset was saved as `data/version_2/candy_data.csv`.
- Duplicate and mismatch validation was included as part of the join logic.

### Exploratory & Visual Analysis

- `pyg.ipynb` contains exploratory analysis with `pygwalker` and `plotly`, including a box plot for `Unit Price` distribution.
- `edvart.ipynb` uses the `edvart` library for automated data reporting and dataset profiling.
- `visuals/` contains notebook-driven visualizations and an interactive `pivottablejs.html` file.

### Feature Engineering

- `feature_engineering/` includes notebooks for factory-level, product-level, and target-level feature creation.
- The notebooks likely generate derived fields to support dashboard metrics and segmentation.

## Dependencies

The Python environment is defined in `requirements.txt` and includes:

- pandas
- numpy
- matplotlib
- seaborn
- plotly
- scikit-learn
- pivottablejs
- jupyter-related packages
- `pygwalker` and `edvart` usage inferred from notebooks

## Project Strengths

- Strong end-to-end workflow from raw data through cleaning and dashboard reporting
- Clear use of data validation and mismatch reporting
- Versioned dataset structure enables repeatable data engineering
- Final deliverables include Power BI dashboard and PDF report
- Supports location analytics via U.S. ZIP code metadata

## Recommended Next Steps

1. Add a summary notebook or README documenting the final business questions and key insights.
2. Expand the final dashboard metrics to include profitability by division, regional sales trends, and factory production performance.
3. Use the consolidated dataset in `data/version_2/candy_data.csv` for advanced forecasting or segmentation.
4. Add a `README.md` to this folder describing the workflow and how to run the notebooks.

## Notes

- The project is centered on candy product sales, factory production, and territory/region performance.
- The available documentation is primarily in notebooks and a data dictionary CSV.
- The final Power BI report is present, but the source PBIX contents require Power BI Desktop to inspect further.
