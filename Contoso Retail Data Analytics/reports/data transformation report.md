# Data Transformation Report

## Overview

Applied transformations on cleaned retail data to create enriched analytics-ready datasets.

## Transformed Files

| File | Description |
|------|-------------|
| `Sales_Enriched.csv` | Master table: all sales with joined dimensions + calculated fields |
| `Monthly_Sales_by_Category.csv` | Monthly revenue/profit/units by product category |
| `Sales_by_Country.csv` | Revenue/profit by store country |
| `Top_10_Products.csv` | Top 10 products by revenue |
| `Sales_by_Store_Type.csv` | Online vs Physical store comparison |
| `Monthly_Trend.csv` | Monthly revenue & profit time series |

## Transformations Applied

1. **[Input]** Loaded 62884 sales, 8065 customers, 2517 products, 67 stores, 11215 exchange rates
2. **[Join]** Merged Products into Sales on ProductKey
3. **[Join]** Merged Customers into Sales on CustomerKey
4. **[Join]** Merged Stores into Sales on StoreKey
5. **[Calc]** Added Revenue = Quantity * Unit Price USD
6. **[Calc]** Added Cost = Quantity * Unit Cost USD
7. **[Calc]** Added Profit = Revenue - Cost
8. **[Calc]** Added Profit Margin %
9. **[Calc]** Added Delivery Days = Delivery Date - Order Date
10. **[Calc]** Added Customer Age at time of order
11. **[Calc]** Added date features: Year, Month, Day, DayOfWeek, Quarter
12. **[Transform]** Merged exchange rates for USD, CAD, EUR, GBP, AUD
13. **[Calc]** Converted Revenue to USD using daily exchange rates
14. **[Calc]** Converted Cost and Profit to USD
15. **[Transform]** Added Store Type (Online vs Physical)
16. **[Transform]** Added Price Tier based on Unit Price: Budget (<50), Mid (50-200), Premium (200-500), Luxury (500+)
17. **[Output]** Saved enriched sales table: Sales_Enriched.csv
18. **[Aggregate]** Created monthly sales by category
19. **[Aggregate]** Created sales by country
20. **[Aggregate]** Created top 10 products by revenue
21. **[Aggregate]** Created sales by store type (Online vs Physical)
22. **[Aggregate]** Created monthly revenue/profit trend

## Key Business Insights Enabled

- **Revenue in USD**: Multi-currency sales normalized to USD for global comparison
- **Profitability**: Profit and margin calculated at line-item level
- **Customer Demographics**: Age, gender, and location now analyzable per order
- **Delivery Performance**: Delivery days calculated to measure logistics efficiency
- **Time Intelligence**: Date parts extracted for trend, seasonality, and cohort analysis
- **Catalog Analysis**: Price tiers enable segmentation by product value
- **Channel Comparison**: Online vs Physical store performance directly comparable

## Files Location

- Raw data: `data/`
- Cleaned data: `cleaned data/`
- Transformed data: `transformed data/`