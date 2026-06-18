import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
orders = pd.read_csv("Data/olist_orders_dataset.csv")
payments = pd.read_csv("Data/olist_order_payments_dataset.csv")
customers = pd.read_csv("Data/olist_customers_dataset.csv")
products = pd.read_csv("Data/olist_products_dataset.csv")
order_items = pd.read_csv("Data/olist_order_items_dataset.csv")

print("="*50)
print("DATASET SHAPES")
print("="*50)

print("Orders:", orders.shape)
print("Payments:", payments.shape)
print("Customers:", customers.shape)
print("Products:", products.shape)
print("Order Items:", order_items.shape)

# ------------------------------
# BUSINESS METRICS
# ------------------------------

total_orders = orders["order_id"].nunique()

total_revenue = payments["payment_value"].sum()

avg_order_value = total_revenue / total_orders

print("\n")
print("="*50)
print("BUSINESS METRICS")
print("="*50)

print("Total Orders:", total_orders)
print("Total Revenue:", round(total_revenue, 2))
print("Average Order Value:", round(avg_order_value, 2))

# ------------------------------
# DATE CONVERSION
# ------------------------------

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"]
)

# ------------------------------
# MONTHLY SALES TREND
# ------------------------------

monthly_orders = orders.groupby(
    orders["order_purchase_timestamp"].dt.to_period("M")
).size()

plt.figure(figsize=(12,5))
monthly_orders.plot()

plt.title("Monthly Orders Trend")
plt.xlabel("Month")
plt.ylabel("Orders")
plt.tight_layout()

plt.savefig("monthly_orders.png")
plt.show()

# ------------------------------
# PAYMENT DISTRIBUTION
# ------------------------------

plt.figure(figsize=(8,8))

payments["payment_type"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Payment Method Distribution")
plt.ylabel("")

plt.savefig("payment_distribution.png")
plt.show()

# ------------------------------
# TOP CUSTOMER STATES
# ------------------------------

top_states = customers["customer_state"].value_counts().head(10)

plt.figure(figsize=(10,5))

top_states.plot(kind="bar")

plt.title("Top Customer States")
plt.xlabel("State")
plt.ylabel("Customers")

plt.tight_layout()

plt.savefig("customer_states.png")
plt.show()

# ------------------------------
# DELIVERY ANALYSIS
# ------------------------------

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.days

print("\nAverage Delivery Days:",
      round(orders["delivery_days"].mean(),2))

# ------------------------------
# REVENUE BY PAYMENT TYPE
# ------------------------------

payment_revenue = payments.groupby(
    "payment_type"
)["payment_value"].sum()

plt.figure(figsize=(8,5))

payment_revenue.plot(kind="bar")

plt.title("Revenue by Payment Type")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig("revenue_by_payment_type.png")
plt.show()