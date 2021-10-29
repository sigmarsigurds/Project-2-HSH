CREATE TABLE IF NOT EXISTS Product(
    id serial PRIMARY KEY,
    merchant_id INTEGER,
    name VARCHAR(255) NOT NULL,
    price NUMERIC,
    quantity INTEGER,
    reserved INTEGER DEFAULT VALUE 0
)
