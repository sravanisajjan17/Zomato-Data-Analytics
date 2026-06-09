-- Zomato Data Analysis — SQL
-- Author: Sravani Sajjan
-- Run against: zomato.db (SQLite) or any SQL DB

-- ── 1. KPI SUMMARY ───────────────────────────────────────
SELECT
    COUNT(*)                                                          AS total_orders,
    SUM(CASE WHEN order_status='Delivered' THEN 1 ELSE 0 END)        AS delivered,
    SUM(CASE WHEN order_status='Cancelled' THEN 1 ELSE 0 END)        AS cancelled,
    ROUND(AVG(order_amount), 2)                                       AS avg_order_value,
    ROUND(SUM(CASE WHEN order_status='Delivered' THEN net_revenue END), 2) AS total_revenue,
    ROUND(AVG(CASE WHEN order_status='Delivered' THEN delivery_time END), 1) AS avg_delivery_min
FROM orders;

-- ── 2. REVENUE BY CITY ───────────────────────────────────
SELECT city,
    COUNT(*)                                                          AS orders,
    ROUND(SUM(CASE WHEN order_status='Delivered' THEN net_revenue END), 2) AS revenue,
    ROUND(AVG(order_amount), 2)                                       AS avg_order_value
FROM orders
GROUP BY city
ORDER BY revenue DESC;

-- ── 3. TOP CUISINES ──────────────────────────────────────
SELECT cuisine,
    COUNT(*)                                                          AS orders,
    ROUND(SUM(CASE WHEN order_status='Delivered' THEN net_revenue END), 2) AS revenue,
    ROUND(AVG(rating), 2)                                             AS avg_rating
FROM orders
GROUP BY cuisine
ORDER BY orders DESC
LIMIT 8;

-- ── 4. CANCELLATION RATE BY RESTAURANT TYPE ──────────────
SELECT restaurant_type,
    COUNT(*)                                                          AS total_orders,
    SUM(CASE WHEN order_status='Cancelled' THEN 1 ELSE 0 END)        AS cancelled,
    ROUND(SUM(CASE WHEN order_status='Cancelled' THEN 1.0 ELSE 0 END)
          / COUNT(*) * 100, 1)                                        AS cancel_pct
FROM orders
GROUP BY restaurant_type
ORDER BY cancel_pct DESC;

-- ── 5. PAYMENT MODE ANALYSIS ─────────────────────────────
SELECT payment_mode,
    COUNT(*)                                                          AS orders,
    ROUND(AVG(order_amount), 2)                                       AS avg_order_value,
    ROUND(SUM(CASE WHEN order_status='Delivered' THEN net_revenue END), 2) AS revenue
FROM orders
GROUP BY payment_mode
ORDER BY revenue DESC;

-- ── 6. CUSTOMER SEGMENTATION ─────────────────────────────
SELECT
    CASE WHEN order_count = 1            THEN 'One-Time'
         WHEN order_count BETWEEN 2 AND 4 THEN 'Regular'
         ELSE                                 'Loyal'
    END                                                               AS segment,
    COUNT(*)                                                          AS customers,
    ROUND(AVG(total_spend), 2)                                        AS avg_spend
FROM (
    SELECT customer_id,
           COUNT(*)         AS order_count,
           SUM(net_revenue) AS total_spend
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
)
GROUP BY segment
ORDER BY avg_spend DESC;

-- ── 7. PEAK ORDERING HOURS ───────────────────────────────
SELECT hour,
    COUNT(*)                         AS orders,
    ROUND(AVG(order_amount), 2)      AS avg_order_value
FROM orders
GROUP BY hour
ORDER BY orders DESC
LIMIT 5;

-- ── 8. MONTHLY REVENUE TREND ─────────────────────────────
SELECT year, month,
    COUNT(*)                                                          AS orders,
    ROUND(SUM(CASE WHEN order_status='Delivered' THEN net_revenue END), 2) AS revenue
FROM orders
GROUP BY year, month
ORDER BY year, month;

-- ── 9. ROLLING 3-MONTH AVG REVENUE (Window Function) ─────
SELECT year, month,
    ROUND(monthly_rev, 2)                                             AS revenue,
    ROUND(AVG(monthly_rev) OVER (
        ORDER BY year, month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2)                                                             AS rolling_3m_avg
FROM (
    SELECT year, month,
           SUM(CASE WHEN order_status='Delivered' THEN net_revenue END) AS monthly_rev
    FROM orders
    GROUP BY year, month
)
ORDER BY year, month;

-- ── 10. TOP 5 RESTAURANTS BY REVENUE ─────────────────────
SELECT restaurant_id,
    COUNT(*)                                                          AS orders,
    ROUND(SUM(CASE WHEN order_status='Delivered' THEN net_revenue END), 2) AS revenue,
    ROUND(AVG(rating), 2)                                             AS avg_rating,
    ROUND(AVG(delivery_time), 1)                                      AS avg_delivery_min
FROM orders
GROUP BY restaurant_id
ORDER BY revenue DESC
LIMIT 5;
