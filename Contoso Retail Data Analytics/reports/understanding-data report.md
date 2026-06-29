# Understanding Data Report

## Dataset Overview

This dataset represents a **retail sales database** with **6 CSV files** containing transactional, customer, product, store, and currency data.

---

## 1. Data Dictionary (Lookup Reference)

The `Data_Dictionary.csv` explains all fields across the 6 tables.

---

## 2. Customers (`Customers.csv`)

| Column | Type | Description |
|--------|------|-------------|
| CustomerKey | int | Primary key |
| Gender | str | Male / Female |
| Name | str | Customer full name |
| City | str | Customer city |
| State Code | str | Abbreviated state |
| State | str | Full state name |
| Zip Code | int | Postal code |
| Country | str | Country |
| Continent | str | Continent |
| Birthday | date | Date of birth |

- **All customers are from Australia** (all rows in sample)
- **States**: New South Wales, Victoria, Queensland, South Australia, Western Australia, Tasmania, Northern Territory, Australian Capital Territory
- **Date range**: Birthdays from 1935 to 2001

---

## 3. Products (`Products.csv`)

| Column | Type | Description |
|--------|------|-------------|
| ProductKey | int | Primary key |
| Product Name | str | Full product name |
| Brand | str | Brand (Contoso, Wide World Importers, Northwind Traders, etc.) |
| Color | str | Product color |
| Unit Cost USD | float | Cost to produce |
| Unit Price USD | float | List price |
| SubcategoryKey | str | Links to subcategory |
| Subcategory | str | Subcategory name |
| CategoryKey | str | Links to category |
| Category | str | Category name |

### Categories:
1. **Audio** (01) — MP3/MP4 players, Recording Pens, Bluetooth Headphones
2. **TV and Video** (02) — Televisions, VCD & DVD, Home Theater Systems, Car Video
3. **Computers** (03) — Laptops, Desktops

**Brands**: Contoso, Wide World Importers, Northwind Traders, Adventure Works, Southridge Video, Litware, Fabrikam, Proseware

---

## 4. Stores (`Stores.csv`)

| Column | Type | Description |
|--------|------|-------------|
| StoreKey | int | Primary key |
| Country | str | Country (Australia, Canada, France, Germany, Italy, Netherlands, UK, USA) + Online |
| State | str | State/province |
| Square Meters | int | Store size |
| Open Date | date | When store opened |

- **67 stores** across 8 countries + **Online** store (StoreKey = 0)
- Store sizes range from **245 to 2100 sq meters**
- **Online store** has no square meter data

---

## 5. Sales (`Sales.csv`) — Core Transaction Table

| Column | Type | Description |
|--------|------|-------------|
| Order Number | int | Unique order ID |
| Line Item | int | Line item within order |
| Order Date | date | When ordered |
| Delivery Date | date | When delivered (nullable) |
| CustomerKey | int | FK to Customers |
| StoreKey | int | FK to Stores |
| ProductKey | int | FK to Products |
| Quantity | int | Units purchased |
| Currency Code | str | Currency (USD, CAD, EUR, GBP, AUD) |

- **Multi-currency transactions** (USD, CAD, EUR, GBP, AUD)
- **Delivery Date** has missing values (orders not yet delivered)
- Each order can have **multiple line items**
- Links to Customers, Stores, and Products via foreign keys

---

## 6. Exchange Rates (`Exchange_Rates.csv`)

| Column | Type | Description |
|--------|------|-------------|
| Date | date | Calendar date |
| Currency | str | Currency code |
| Exchange | float | Rate vs USD |

- **Daily exchange rates** from 2015 to at least 2016
- **5 currencies**: USD (base), CAD, AUD, EUR, GBP
- USD always has Exchange = 1.0

---

## Entity Relationships (Star Schema)

```
Customers ──┐
             ├── Sales ──── Products
Stores ─────┘
                  │
            Exchange_Rates (Date + Currency)
```

- **Sales** is the fact table (transactions)
- **Customers, Stores, Products** are dimension tables
- **Exchange_Rates** supports currency conversion by date

---

## Key Observations

1. **Geography**: Customers are exclusively Australian; stores are global (8 countries + Online).
2. **Missing data**: Delivery dates are blank for many orders — indicates pending/undelivered orders.
3. **Currency diversity**: Sales recorded in 5 currencies — exchange rate table enables USD normalization.
4. **Product breadth**: 3 major categories (Audio, TV/Video, Computers) with multiple brands.
5. **Online store**: StoreKey 0 represents online channel with no physical size.
6. **Composite keys**: Sales uses Order Number + Line Item as natural composite key.
