
-- 🥉 BRONZE LAYER: Raw Table
CREATE TABLE IF NOT EXISTS bike_sales_raw (
    sale_id int,
    date text,
    customer_id int,
    bike_model text,
    price double,
    quantity int,
    store_location text,
    salesperson_id int,
    payment_method text,
    customer_age int,
    customer_gender text,
    PRIMARY KEY (sale_id)
);

-- 🥈 SILVER LAYER: Cleaned Table
CREATE TABLE IF NOT EXISTS bike_sales_cleaned (
    sale_id int,
    date text,
    customer_id int,
    bike_model text,
    price double,
    quantity int,
    store_location text,
    salesperson_id int,
    payment_method text,
    customer_age int,
    customer_gender text,
    PRIMARY KEY (sale_id)
);
