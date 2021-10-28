CREATE TABLE IF NOT EXISTS Merchant(
    id serial PRIMARY KEY,
    name VARCHAR(255),
    ssn VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    phone_number VARCHAR(20),
    allows_discount BOOLEAN DEFAULT FALSE
);
