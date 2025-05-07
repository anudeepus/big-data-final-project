from connect_astra import get_session

session = get_session()

# Create cleaned table
session.execute("""
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
)
""")
rows = session.execute("SELECT * FROM bike_sales_raw")
clean_count = 0
skipped_count = 0

for row in rows:
    if row.price <= 0 or row.quantity <= 0 or row.customer_age <= 0 or row.customer_age > 100:
        skipped_count += 1
        continue

    session.execute("""
        INSERT INTO bike_sales_cleaned (
            sale_id, date, customer_id, bike_model, price, quantity,
            store_location, salesperson_id, payment_method,
            customer_age, customer_gender
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row.sale_id, row.date, row.customer_id, row.bike_model, row.price,
        row.quantity, row.store_location, row.salesperson_id,
        row.payment_method, row.customer_age, row.customer_gender
    ))
    clean_count += 1
    print(f"✅ Cleaned row inserted: Sale_ID={row.sale_id}")
print(f"\n✅ Cleaning complete: {clean_count} rows inserted, {skipped_count} rows skipped.")
