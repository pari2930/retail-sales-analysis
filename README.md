# Retail Sales & Customer Segmentation Analysis

End-to-end analysis of two years of retail sales data across Indian regions — cleaning a messy raw export, answering four business questions in Python, and building an interactive Power BI dashboard on top of the results.

## Business questions answered

1. **Which region is underperforming on profit despite comparable sales?**
2. **Which product category is being over-discounted relative to its margin?**
3. **Which customer segment is actually the most profitable — not just the highest-selling?**
4. **How does monthly sales performance trend over the two-year period?**

## Key findings

- **East region is the clear underperformer.** It has similar total sales to every other region (~₹12.2 Cr) but a profit margin of only **8.1%**, roughly half of West, South, and North (all ~19.7–20.2%). Sales volume alone would have hidden this — it only shows up once profit is broken out by region.
- **Furniture is being discounted past the point of profitability.** Its average discount (15%) is similar to other categories, but its profit margin (14.9%) trails Electronics and Office Supplies (~18.3–18.4%), driven by heavy discounting on already lower-margin items.
- **Home Office is the most profitable segment, not the highest-selling one.** It has the lowest total sales of the three segments but the highest total profit (₹3.43 Cr vs. ₹2.59 Cr for Corporate), because of higher per-order margins.

Full numbers are in [`summary_stats.txt`](summary_stats.txt).

## What's in this repo

| File | Description |
|---|---|
| `raw_sales_data.csv` | Raw export with realistic messiness (duplicates, missing values, mixed date formats, negative-quantity entry errors) |
| `cleaned_sales_data.csv` | Output after the cleaning step below |
| `clean_and_analyze.py` | Pandas cleaning + all four business-question analyses |
| `region_sales_vs_margin.png` | Chart: sales vs. profit margin by region |
| `category_margin.png` | Chart: profit margin by category |
| `segment_profit_share.png` | Chart: profit share by customer segment |
| `monthly_sales_trend.png` | Chart: monthly sales trend |
| `summary_stats.txt` | Region / category / segment summary tables |

## Data cleaning steps

The raw file simulates a realistic export from a reporting system, including:
- ~1.5% exact duplicate rows
- Missing values in `Customer Name`, `Ship Mode`, and `Discount`
- `Order Date` mixed between `YYYY-MM-DD` and `DD/MM/YYYY` formats
- Stray whitespace and inconsistent casing in `Region`
- A handful of negative `Quantity` values from data entry errors

`clean_and_analyze.py` handles all of this: drops duplicates, parses both date formats into one consistent type, strips/normalizes text fields, fixes negative quantities, and fills or drops missing values with a documented rule for each column (e.g. missing discount → 0, missing customer name → row dropped since it can't be attributed).

## Tech stack

- **Python (Pandas, Matplotlib)** — cleaning, aggregation, chart generation
- **Power BI** — interactive dashboard with DAX measures for profit margin and month-over-month growth, and drill-down by region/category/segment

## Dashboard

[Add your Power BI published link here once you publish it]

## How to run

```bash
pip install pandas numpy matplotlib
python clean_and_analyze.py
```

This regenerates `cleaned_sales_data.csv` and all chart PNGs.

---
*Sarvesh Parulekar — [LinkedIn](https://www.linkedin.com/in/sarvesh-parulekar)*
