# 🍽️ Zomato End-to-End Data Analytics Project

**Author:** Sravani Sajjan  
**Tools:** Python · SQL (SQLite) · Power BI  
**Domain:** Food-Tech / Business Analytics

---

## 📌 Project Overview

This project performs a complete end-to-end data analysis on Zomato food delivery data,
covering order trends, restaurant performance, customer behaviour, and revenue analytics.
The pipeline spans data generation → cleaning → SQL analysis → Python EDA & visualisations → Power BI dashboard.

---

## 🗂️ Project Structure

```
zomato_project/
│
├── data/
│   ├── generate_data.py        # Synthetic dataset generator (1,000 orders)
│   ├── zomato_orders.csv       # Raw dataset
│   ├── zomato_cleaned.csv      # Cleaned & feature-engineered dataset
│   └── zomato.db               # SQLite database
│
├── python/
│   ├── zomato_eda.py           # Data cleaning, EDA, visualisations
│   └── run_sql_analysis.py     # Loads data into SQLite & runs all queries
│
├── sql/
│   ├── 01_schema.sql           # DDL — table creation & indexes
│   └── 02_analysis_queries.sql # 14 analytical SQL queries
│
├── outputs/
│   ├── fig1_overview.png       # Overview charts (4-panel)
│   ├── fig2_trends.png         # Trend & performance charts (4-panel)
│   └── sql_query_results.xlsx  # All SQL results in Excel (10 sheets)
│
└── zomato_dashboard.pbix       # Power BI Dashboard (pre-built)
```

---

## 🔄 End-to-End Pipeline

```
Raw Data
   ↓
[Python] Data Cleaning & Feature Engineering
   ↓
[Python] Exploratory Data Analysis + Visualisations
   ↓
[SQL]    Schema Creation → Data Loading → Analytical Queries
   ↓
[Power BI] Interactive Dashboard
```

---

## 📊 Key Business Metrics Analysed

| Area | Metrics |
|---|---|
| Revenue | Total, monthly trend, rolling 3-month avg, by city/cuisine |
| Orders | Volume, delivery rate, cancellation rate, peak hours |
| Restaurants | Top performers, hidden gems (high rating × low orders), city rank |
| Customers | Segmentation (One-Time / Occasional / Regular / Loyal), repeat rate |
| Operations | Avg delivery time by city, online vs offline, payment mode split |

---

## 🐍 Python Module Highlights

**Data Cleaning**
- Removed duplicates and negative revenue rows
- Capped delivery time outliers at 90 min
- Created `rating_band` feature (Poor / Average / Good / Excellent)

**EDA & KPIs**
- 991 orders analysed across 8 cities, 10 cuisines, 6 restaurant types
- Delivery rate: **80.5%** | Cancellation rate: **15.3%**
- Total revenue: **₹9,66,545** | Avg order value: **₹1,312**
- Avg delivery time: **51.5 min**

**Visualisations** (8 charts across 2 figures)
- Revenue by City (horizontal bar)
- Order Status Distribution (donut pie)
- Orders by Cuisine (bar)
- Payment Mode Split (bar)
- Monthly Revenue Trend (line + fill)
- Avg Delivery Time by City (horizontal bar)
- Day × Hour Heatmap (seaborn heatmap)
- Rating Distribution (histogram)

---

## 🗃️ SQL Module Highlights

**Schema:** 3 normalised tables — `restaurants`, `customers`, `orders`  
**Queries:** 14 analytical queries including:

- KPI summary with delivery/cancellation rates
- Revenue by city, cuisine, restaurant type
- Monthly + rolling 3-month revenue trend
- Top 10 restaurants by revenue
- Hidden gem restaurants (high rating, low volume)
- Customer segmentation (4 tiers by order frequency)
- Peak ordering hours analysis
- Discount impact on cancellations
- Window function: `RANK()` per city, `AVG() OVER` rolling window

---

## 📈 Power BI Dashboard

The included `.pbix` file contains an interactive dashboard with:
- Revenue KPI cards
- City-wise and cuisine-wise breakdown
- Monthly trend line chart
- Restaurant type analysis
- Filter slicers by city, cuisine, and order status

---

## ▶️ How to Run

```bash
# 1. Generate raw data
python data/generate_data.py

# 2. Run EDA + visualisations
python python/zomato_eda.py

# 3. Load into SQLite and run SQL analysis
python python/run_sql_analysis.py

# 4. Open Power BI
# Open zomato_dashboard.pbix in Power BI Desktop
```

**Requirements:** `pandas numpy matplotlib seaborn openpyxl sqlite3`

---

## 💡 Key Insights

1. **Delhi and Pune** are the top revenue-generating cities, together contributing ~37% of total revenue.
2. **Fine Dining** has the highest cancellation rate (20.8%) — possible mismatch in delivery expectations.
3. **North Indian and Mughlai** cuisines lead in both order volume and revenue.
4. **UPI is the top payment mode** (26.4% of orders) — aligns with India's digital payment trend.
5. **Loyal customers** (7+ orders) spend ~8.7× more than one-time customers on average.
6. Orders are distributed evenly across hours — no single dominant peak window.
