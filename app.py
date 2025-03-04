# import streamlit as st
# import razorpay
# import sqlite3

# # Razorpay API Keys
# RAZORPAY_KEY_ID = "your_key_id"
# RAZORPAY_KEY_SECRET = "your_key_secret"

# client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# # Database connection
# conn = sqlite3.connect("users.db", check_same_thread=False)
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, amount INTEGER, status TEXT)")
# conn.commit()

# st.title("🔹 Registration & Payment Portal")

# # User Registration Form
# name = st.text_input("Full Name")
# email = st.text_input("Email")
# amount = st.number_input("Amount (INR)", min_value=10)

# if st.button("Proceed to Payment"):
#     order = client.order.create({
#         "amount": int(amount * 100),  # Convert to paisa
#         "currency": "INR",
#         "payment_capture": "1",
#     })

#     # Insert user details in database (status = 'Pending')
#     cursor.execute("INSERT INTO users (name, email, amount, status) VALUES (?, ?, ?, ?)", (name, email, amount, "Pending"))
#     conn.commit()

#     st.success("Click below to complete the payment")
#     st.markdown(f"[Pay Now](https://razorpay.com/pay/{order['id']})", unsafe_allow_html=True)

# # Display Payment Status
# st.subheader("📝 Payment Status")
# users = cursor.execute("SELECT name, email, status FROM users").fetchall()
# for user in users:
#     st.write(f"👤 {user[0]} | 📧 {user[1]} | Status: {user[2]}")

# conn.close()
import streamlit as st
import razorpay
import sqlite3

# Razorpay API Keys
RAZORPAY_KEY_ID = "your_key_id"
RAZORPAY_KEY_SECRET = "your_key_secret"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Database connection
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, amount INTEGER, status TEXT)")
conn.commit()

st.title("🔹 UPI Payment Registration Portal")

# User Input
name = st.text_input("Full Name")
email = st.text_input("Email")
amount = st.number_input("Amount (INR)", min_value=10)

if st.button("Pay via UPI"):
    order = client.order.create({
        "amount": int(amount * 100),  # Convert to paisa
        "currency": "INR",
        "payment_capture": "1",
        "method": "upi"  # 🔥 Enable UPI payments
    })

    # Save user with status "Pending"
    cursor.execute("INSERT INTO users (name, email, amount, status) VALUES (?, ?, ?, ?)", (name, email, amount, "Pending"))
    conn.commit()

    st.success("Scan QR Code or use the UPI Link below:")
    st.markdown(f"[Pay Now via UPI](https://razorpay.com/pay/{order['id']})", unsafe_allow_html=True)

st.subheader("📝 Payment Status")
users = cursor.execute("SELECT name, email, status FROM users").fetchall()
for user in users:
    st.write(f"👤 {user[0]} | 📧 {user[1]} | Status: {user[2]}")

conn.close()
