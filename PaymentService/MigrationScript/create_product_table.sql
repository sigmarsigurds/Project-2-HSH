CREATE TABLE IF NOT EXISTS Payment_Transaction(
    id serial PRIMARY KEY,
    order_id INTEGER,
    success BOOLEAN
)
