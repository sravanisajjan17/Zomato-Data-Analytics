# Zomato End-to-End Data Analysis
# Author: Sravani Sajjan
# Tools : Python, Pandas, NumPy, Matplotlib, Seaborn, SQLite

import pandas as pd
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3, warnings
warnings.filterwarnings('ignore')

RED = '#E23744'; ACC = '#F5A623'
PAL = [RED, ACC, '#2E86AB', '#A23B72', '#F18F01', '#44BBA4', '#C73E1D', '#393E41']

# ── 1. GENERATE DATA ─────────────────────────────────────
np.random.seed(42)
n = 500
cities   = ['Mumbai','Delhi','Bangalore','Hyderabad','Chennai','Pune']
cuisines = ['North Indian','South Indian','Chinese','Fast Food','Biryani','Pizza','Mughlai','Seafood']
r_types  = ['Quick Bites','Casual Dining','Café','Fine Dining','Food Court']
pay_mode = ['Online','Cash','Card','UPI']

dates = pd.date_range('2023-01-01', '2024-12-31', periods=n)
df = pd.DataFrame({
    'order_id':        [f'ORD{i:04d}' for i in range(n)],
    'customer_id':     [f'C{np.random.randint(1,200):03d}' for _ in range(n)],
    'restaurant_id':   [f'R{np.random.randint(1,100):03d}' for _ in range(n)],
    'city':            np.random.choice(cities, n),
    'cuisine':         np.random.choice(cuisines, n),
    'restaurant_type': np.random.choice(r_types, n),
    'order_date':      np.random.choice(dates, n),
    'order_amount':    np.round(np.random.uniform(150, 2500, n), 2),
    'delivery_fee':    np.round(np.random.uniform(0, 80, n), 2),
    'discount':        np.round(np.random.uniform(0, 300, n), 2),
    'payment_mode':    np.random.choice(pay_mode, n),
    'order_status':    np.random.choice(['Delivered','Cancelled','Pending'], n, p=[0.80,0.15,0.05]),
    'delivery_time':   np.random.randint(15, 90, n),
    'rating':          np.round(np.random.uniform(2.5, 5.0, n), 1),
})
df['net_revenue'] = df['order_amount'] + df['delivery_fee'] - df['discount']
df['month'] = pd.to_datetime(df['order_date']).dt.month
df['year']  = pd.to_datetime(df['order_date']).dt.year
df['hour']  = np.random.randint(0, 24, n)
df['day']   = pd.to_datetime(df['order_date']).dt.day_name()

# ── 2. CLEAN ─────────────────────────────────────────────
df.drop_duplicates(inplace=True)
df = df[df['net_revenue'] > 0]
df['delivery_time'] = df['delivery_time'].clip(upper=90)
df['rating_band'] = pd.cut(df['rating'], bins=[0,3,4,5], labels=['Low','Mid','High'])
print(f"✅ Data ready: {df.shape[0]} rows\n")

# ── 3. KPIs ───────────────────────────────────────────────
del_ = df[df['order_status']=='Delivered']
print(f"Total Orders   : {len(df)}")
print(f"Delivered      : {len(del_)} ({len(del_)/len(df)*100:.1f}%)")
print(f"Total Revenue  : ₹{del_['net_revenue'].sum():,.0f}")
print(f"Avg Order Value: ₹{df['order_amount'].mean():,.0f}")
print(f"Avg Rating     : {df['rating'].mean():.2f}")
print(f"Avg Delivery   : {del_['delivery_time'].mean():.1f} min\n")

# ── 4. VISUALISATIONS ────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
fig.suptitle('Zomato Order Analytics', fontsize=15, fontweight='bold', color='#1C1C1C')

# Revenue by City
city_rev = del_.groupby('city')['net_revenue'].sum().sort_values()
axes[0,0].barh(city_rev.index, city_rev.values, color=PAL[:len(city_rev)])
axes[0,0].set_title('Revenue by City')

# Order Status Pie
sc = df['order_status'].value_counts()
axes[0,1].pie(sc, labels=sc.index, autopct='%1.1f%%',
              colors=[RED, ACC, '#AAA'], wedgeprops=dict(width=0.6), startangle=140)
axes[0,1].set_title('Order Status')

# Top Cuisines
tc = df['cuisine'].value_counts().head(6)
axes[0,2].bar(tc.index, tc.values, color=PAL); axes[0,2].set_title('Top Cuisines')
axes[0,2].set_xticklabels(tc.index, rotation=30, ha='right')

# Monthly Revenue Trend
monthly = del_.groupby(['year','month'])['net_revenue'].sum().reset_index()
monthly['period'] = monthly['year'].astype(str)+'-'+monthly['month'].astype(str).str.zfill(2)
axes[1,0].plot(monthly['period'], monthly['net_revenue']/1000, marker='o', color=RED, linewidth=2)
axes[1,0].fill_between(range(len(monthly)), monthly['net_revenue']/1000, alpha=0.15, color=RED)
axes[1,0].set_title('Monthly Revenue (₹K)')
axes[1,0].set_xticks(range(0, len(monthly), 3))
axes[1,0].set_xticklabels(monthly['period'][::3], rotation=45, ha='right', fontsize=7)

# Day × Hour Heatmap
heat = df.groupby(['day','hour']).size().unstack(fill_value=0)
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
heat = heat.reindex([d for d in day_order if d in heat.index])
sns.heatmap(heat, ax=axes[1,1], cmap='YlOrRd', cbar_kws={'shrink':0.8})
axes[1,1].set_title('Orders: Day × Hour')

# Rating Distribution
axes[1,2].hist(df['rating'], bins=15, color=RED, edgecolor='white', alpha=0.85)
axes[1,2].axvline(df['rating'].mean(), color='black', linestyle='--',
                  label=f"Mean: {df['rating'].mean():.2f}")
axes[1,2].set_title('Rating Distribution'); axes[1,2].legend()

plt.tight_layout()
plt.savefig('zomato_charts.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart saved: zomato_charts.png\n")

# ── 5. SQLITE ────────────────────────────────────────────
conn = sqlite3.connect('zomato.db')
df.to_sql('orders', conn, if_exists='replace', index=False)

queries = {
    'Revenue by City':    "SELECT city, ROUND(SUM(net_revenue),2) AS revenue, COUNT(*) AS orders FROM orders WHERE order_status='Delivered' GROUP BY city ORDER BY revenue DESC",
    'Top Cuisines':       "SELECT cuisine, COUNT(*) AS orders FROM orders GROUP BY cuisine ORDER BY orders DESC LIMIT 5",
    'Cancel by Type':     "SELECT restaurant_type, ROUND(SUM(CASE WHEN order_status='Cancelled' THEN 1.0 ELSE 0 END)/COUNT(*)*100,1) AS cancel_pct FROM orders GROUP BY restaurant_type ORDER BY cancel_pct DESC",
    'Payment Mode':       "SELECT payment_mode, COUNT(*) AS orders, ROUND(AVG(order_amount),0) AS avg_value FROM orders GROUP BY payment_mode ORDER BY orders DESC",
    'Customer Segments':  "SELECT CASE WHEN c<2 THEN 'One-Time' WHEN c<5 THEN 'Regular' ELSE 'Loyal' END seg, COUNT(*) customers FROM (SELECT customer_id, COUNT(*) c FROM orders WHERE order_status='Delivered' GROUP BY customer_id) GROUP BY seg",
}

for name, sql in queries.items():
    print(f"── {name}\n{pd.read_sql(sql, conn).to_string(index=False)}\n")

conn.close()
print("✅ SQLite analysis complete")
