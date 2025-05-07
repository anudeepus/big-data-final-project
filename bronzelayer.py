from connect_astra import get_session
import csv
session = get_session()
session.execute("""
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
)
""")
with open("bike_sales_100k.csv", "r") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=1):  # i = row counter
        try:
            session.execute("""
                INSERT INTO bike_sales_raw (
                    sale_id, date, customer_id, bike_model, price, quantity,
                    store_location, salesperson_id, payment_method,
                    customer_age, customer_gender
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                int(row['Sale_ID']), row['Date'], int(row['Customer_ID']),
                row['Bike_Model'], float(row['Price']), int(row['Quantity']),
                row['Store_Location'], int(row['Salesperson_ID']),
                row['Payment_Method'], int(row['Customer_Age']),
                row['Customer_Gender']
            ))
            print(f"✅ Inserted row {i}: Sale_ID={row['Sale_ID']}")
        except Exception as e:
            print(f"❌ Error inserting row {i} (Sale_ID={row['Sale_ID']}): {e}")
