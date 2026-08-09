"""
Retail Sales & Customer Segmentation Analysis
Cleans the raw export and answers four business questions using Pandas.
Outputs a cleaned CSV and PNG charts to /outputs for use in the Power BI
dashboard and the README.
"""

import pandas as pd
import matplotlib.pyplot as plt

RAW_PATH = "/home/claude/project/data/raw_sales_data.csv"
CLEAN_PATH = "/home/claude/project/data/cleaned_sales_data.csv"
OUT_DIR = "/home/claude/project/outputs"

df = pd.read_csv(RAW_PATH)
print(f"Raw rows: {len(df)}")

# --- 1. Clean ---

# Drop exact duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"Dropped {before - len(df)} duplicate rows")

# Standardize Order Date to a single format (mixed YYYY-MM-DD / DD/MM/YYYY)
def parse_date(val):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return pd.to_datetime(val, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

df["Order Date"] = df["Order Date"].apply(parse_date)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%Y-%m-%d", errors="coerce")

# Clean stray whitespace/casing in Region
df["Region"] = df["Region"].astype(str).str.strip().str.title()

# Fix negative quantities (data entry errors) -> take absolute value
df["Quantity"] = df["Quantity"].abs()

# Fill missing Discount with 0 (no discount applied), missing Ship Mode with "Standard"
df["Discount"] = df["Discount"].fillna(0)
df["Ship Mode"] = df["Ship Mode"].fillna("Standard")

# Drop rows where Customer Name is missing (can't attribute to a customer)
before = len(df)
df = df.dropna(subset=["Customer Name"])
print(f"Dropped {before - len(df)} rows with missing customer name")

# Add derived columns useful for analysis
df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)
df["Profit Margin"] = (df["Profit"] / df["Sales"]).round(3)

df.to_csv(CLEAN_PATH, index=False)
print(f"Clean rows: {len(df)}")

# --- 2. Business Question 1: Which region underperforms on profit despite high sales? ---
region_summary = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
).round(0)
region_summary["Profit Margin %"] = (region_summary["Total_Profit"] / region_summary["Total_Sales"] * 100).round(1)
region_summary = region_summary.sort_values("Total_Sales", ascending=False)
print("\n=== Region Summary ===")
print(region_summary)

fig, ax1 = plt.subplots(figsize=(8, 5))
region_summary["Total_Sales"].plot(kind="bar", ax=ax1, color="#1F3864", alpha=0.85, position=1, width=0.4)
ax2 = ax1.twinx()
region_summary["Profit Margin %"].plot(kind="line", ax=ax2, color="#D9822B", marker="o", linewidth=2)
ax1.set_ylabel("Total Sales (INR)")
ax2.set_ylabel("Profit Margin %")
ax1.set_title("Sales vs. Profit Margin by Region")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/region_sales_vs_margin.png", dpi=150)
plt.close()

# --- 3. Business Question 2: Which category should get more/less discount? ---
cat_discount = df.groupby("Category").agg(
    Avg_Discount=("Discount", "mean"),
    Total_Profit=("Profit", "sum"),
    Total_Sales=("Sales", "sum"),
).round(2)
cat_discount["Profit Margin %"] = (cat_discount["Total_Profit"] / cat_discount["Total_Sales"] * 100).round(1)
print("\n=== Category Discount Impact ===")
print(cat_discount)

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(cat_discount.index, cat_discount["Profit Margin %"], color="#1F3864")
ax.set_ylabel("Profit Margin %")
ax.set_title("Profit Margin by Category")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/category_margin.png", dpi=150)
plt.close()

# --- 4. Business Question 3: Which customer segment is most valuable? ---
segment_summary = df.groupby("Segment").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Avg_Order_Value=("Sales", "mean"),
    Orders=("Order ID", "nunique"),
).round(0)
segment_summary = segment_summary.sort_values("Total_Profit", ascending=False)
print("\n=== Segment Summary ===")
print(segment_summary)

fig, ax = plt.subplots(figsize=(7, 5))
ax.pie(segment_summary["Total_Profit"].clip(lower=0), labels=segment_summary.index, autopct="%1.0f%%",
       colors=["#1F3864", "#4472C4", "#8FAADC"])
ax.set_title("Share of Total Profit by Customer Segment")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/segment_profit_share.png", dpi=150)
plt.close()

# --- 5. Business Question 4: How does monthly performance trend look (YoY growth)? ---
monthly = df.groupby("Order Month").agg(Total_Sales=("Sales", "sum")).reset_index()
monthly = monthly.sort_values("Order Month")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly["Order Month"], monthly["Total_Sales"], color="#1F3864", marker="o")
ax.set_title("Monthly Sales Trend (2023-2024)")
ax.set_ylabel("Total Sales (INR)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/monthly_sales_trend.png", dpi=150)
plt.close()

# --- Save summary tables for README ---
with open(f"{OUT_DIR}/summary_stats.txt", "w") as f:
    f.write("REGION SUMMARY\n")
    f.write(region_summary.to_string())
    f.write("\n\nCATEGORY DISCOUNT IMPACT\n")
    f.write(cat_discount.to_string())
    f.write("\n\nSEGMENT SUMMARY\n")
    f.write(segment_summary.to_string())

print("\nDone. Charts and summary saved to /outputs")
