-- Open output/sales.db in a SQLite client and run these queries.
-- 1. Total sales revenue
SELECT ROUND(SUM(total), 2) AS revenue FROM sales;

-- 2. Revenue by product
SELECT product, COUNT(*) AS orders, ROUND(SUM(total), 2) AS revenue
FROM sales GROUP BY product ORDER BY revenue DESC;

-- 3. Check for duplicate order IDs (should return no rows)
SELECT order_id, COUNT(*) AS occurrences
FROM sales GROUP BY order_id HAVING COUNT(*) > 1;

-- 4. Check for inconsistent totals (should return no rows)
SELECT * FROM sales WHERE ABS(total - ROUND(quantity * price, 2)) > 0.001;
