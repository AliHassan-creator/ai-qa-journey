-- Run these 12 SELECT exercises against sample_orders.sql.

-- Query 01: Select all orders.
SELECT order_id, customer_id, order_date, status, order_total
FROM orders;

-- Query 02: Filter orders by one status.
SELECT order_id, order_date, order_total
FROM orders
WHERE status = 'complete';

-- Query 03: Sort newest orders first.
SELECT order_id, order_date, status
FROM orders
ORDER BY order_date DESC;

-- Query 04: Find customers whose names contain 'sample'.
SELECT customer_id, customer_name
FROM customers
WHERE customer_name LIKE '%Sample%';

-- Query 05: Select orders in a chosen set of statuses.
SELECT order_id, status
FROM orders
WHERE status IN ('pending', 'cancelled');

-- Query 06: Select orders in an inclusive date range.
SELECT order_id, order_date
FROM orders
WHERE order_date BETWEEN '2026-10-02' AND '2026-10-05';

-- Query 07: Find customers with a missing phone number.
SELECT customer_id, customer_name
FROM customers
WHERE phone IS NULL;

-- Query 08: Calculate common order aggregates.
SELECT COUNT(*) AS order_count,
       SUM(order_total) AS total_value,
       AVG(order_total) AS average_value,
       MIN(order_total) AS minimum_value,
       MAX(order_total) AS maximum_value
FROM orders;

-- Query 09: Group orders by customer and keep customers with at least two.
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 2;

-- Query 10: INNER JOIN orders to the customers who placed them.
SELECT o.order_id, c.customer_name, o.status, o.order_total
FROM orders AS o
INNER JOIN customers AS c ON c.customer_id = o.customer_id;

-- Query 11: LEFT JOIN to find customers who have no orders.
SELECT c.customer_id, c.customer_name
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;

-- Query 12: Join orders, order_items, and products (three tables).
SELECT o.order_id, p.product_name, oi.quantity, oi.unit_price,
       oi.quantity * oi.unit_price AS line_total
FROM orders AS o
INNER JOIN order_items AS oi ON oi.order_id = o.order_id
INNER JOIN products AS p ON p.product_id = oi.product_id;
