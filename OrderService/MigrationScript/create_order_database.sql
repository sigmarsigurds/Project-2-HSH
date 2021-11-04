CREATE TABLE IF NOT EXISTS "CreditCard" (
    card_id SERIAL PRIMARY KEY,
    card_number VARCHAR(50) NOT NULL,
    expiration_month INT NOT NULL,
    expiration_year INT NOT NULL,
    cvc INT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Order" (
    order_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    merchant_id INT NOT NULL,
    buyer_id INT NOT NULL,
    -- card_id INT NOT NULL,
    -- FOREIGN KEY (card_id) REFERENCES "CreditCard" (card_id),
    card_number VARCHAR(255) NOT NULL,
    total_price FLOAT
);