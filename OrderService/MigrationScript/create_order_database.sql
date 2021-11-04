CREATE TABLE IF NOT EXISTS "Order" (
    order_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    merchant_id INT NOT NULL,
    buyer_id INT NOT NULL,
    card_number VARCHAR(255) NOT NULL,
    total_price FLOAT
);