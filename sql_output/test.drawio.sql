CREATE TABLE orders
(
    order_id    INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date  DATE,
    amount      DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);