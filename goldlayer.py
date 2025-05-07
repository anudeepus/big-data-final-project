from connect_astra import get_session
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from collections import defaultdict

session = get_session()
rows = session.execute("SELECT * FROM bike_sales_cleaned")
X_quantity = []
y_quantity = []
bike_models = []
store_locations = []
bike_model_count = defaultdict(int)
store_sales = defaultdict(int)
bike_model_encoder = LabelEncoder()
store_encoder = LabelEncoder()
payment_encoder = LabelEncoder()
bike_list = []
store_list = []
payment_list = []
for row in rows:
    bike_list.append(row.bike_model)
    store_list.append(row.store_location)
    payment_list.append(row.payment_method)
bike_model_encoder.fit(bike_list)
store_encoder.fit(store_list)
payment_encoder.fit(payment_list)
rows = session.execute("SELECT * FROM bike_sales_cleaned")
for row in rows:
    bike_models.append(row.bike_model)
    store_locations.append(row.store_location)
    bike_model_count[row.bike_model] += 1
    store_sales[row.store_location] += int(row.quantity)
    features = [
        int(row.customer_age),
        bike_model_encoder.transform([row.bike_model])[0],
        store_encoder.transform([row.store_location])[0],
        payment_encoder.transform([row.payment_method])[0],
        float(row.price)
    ]
    X_quantity.append(features)
    y_quantity.append(int(row.quantity))
X_train, X_test, y_train, y_test = train_test_split(X_quantity, y_quantity, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
rmse = root_mean_squared_error(y_test, predictions)
print(f"✅ ML Model: Quantity Prediction RMSE = {rmse:.2f}")
top_stores = sorted(store_sales.items(), key=lambda x: x[1], reverse=True)[:10]
store_names = [x[0] for x in top_stores]
store_quantities = [x[1] for x in top_stores]
plt.figure(figsize=(12, 6))
plt.bar(store_names, store_quantities)
plt.title("Top 10 Store Locations by Quantity Sold")
plt.xlabel("Store Location")
plt.ylabel("Total Quantity")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_10_stores.png")
print("📊 Plot 1 saved: top_10_stores.png")
labels = list(bike_model_count.keys())
sizes = list(bike_model_count.values())
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title("Bike Model Distribution")
plt.tight_layout()
plt.savefig("bike_model_pie.png")
print("📊 Plot 2 saved: bike_model_pie.png")
