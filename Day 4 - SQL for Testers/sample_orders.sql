-- Small, fictional orders dataset for local SQL practice.
-- Deliberate data-quality anomalies are documented in run_checks.py.

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    email TEXT,
    phone TEXT
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    current_price REAL NOT NULL CHECK (current_price >= 0)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    order_total REAL NOT NULL CHECK (order_total >= 0),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO customers (customer_id, customer_name, email, phone) VALUES
    (1, 'Asha Sample', 'asha@example.test', '555-0101'),
    (2, 'Bilal Sample', 'bilal@example.test', NULL),
    (3, 'Cleo Sample', 'asha@example.test', '555-0103'),
    (4, 'Dara Sample', 'dara@example.test', NULL),
    (5, 'Evan Sample', 'evan@example.test', '555-0105'),
    (6, 'Fara Sample', 'fara@example.test', NULL);

INSERT INTO products (product_id, product_name, current_price) VALUES
    (1, 'Notebook', 5.00),
    (2, 'Pen', 2.00),
    (3, 'Bag', 20.00);

INSERT INTO orders (order_id, customer_id, order_date, status, order_total) VALUES
    (100, 1, '2026-10-01', 'complete', 14.00),
    (101, 2, '2026-10-02', 'pending', 20.00),
    (102, 2, '2026-10-03', 'complete', 35.00),
    (103, 3, '2026-10-04', 'cancelled', 7.00),
    (104, 5, '2026-10-05', 'complete', 22.00),
    (105, 4, '2026-10-06', 'pending', 0.00);

INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price) VALUES
    (900, 100, 1, 2, 5.00),
    (901, 100, 2, 2, 2.00),
    (902, 101, 3, 1, 20.00),
    (903, 102, 3, 1, 20.00),
    (904, 102, 1, 2, 5.00),
    (905, 103, 1, 1, 7.00),
    (906, 104, 3, 1, 20.00),
    (907, 104, 2, 1, 2.00),
    (908, 999, 1, 1, 5.00),
    (909, 104, 2, 0, 2.00);
