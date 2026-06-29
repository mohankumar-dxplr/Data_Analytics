# Data Cleaning Report

## Summary of Changes

| Table | Original Rows | Cleaned Rows |
|-------|--------------|-------------|
| Sales | 62884 | 62884 |
| Customers | 15266 | 15266 |
| Products | 2517 | 2517 |
| Stores | 67 | 67 |
| Exchange_Rates | 11215 | 11215 |

## Detailed Changes by Table

### Sales

- Delivery Date missing: 49719 rows (kept as NaN — pending delivery)
### Customers

### Products

### Stores

- Square Meters missing for 1 rows (Online store — kept as NaN)
### Exchange_Rates

## Notes

- Raw data is preserved unchanged in the `data/` folder.
- All cleaned files are saved in `cleaned data/` folder.
- Missing `Delivery Date` values in Sales were kept as NaN (orders not yet delivered).
- Missing `Square Meters` for the Online store was kept as NaN.
- Price columns in Products were cleaned from formatted strings ($1,299.99) to numeric floats.
- Date columns were converted to proper datetime types.
- Text columns were trimmed of leading/trailing whitespace.
- Product Color values were title-cased for consistency.