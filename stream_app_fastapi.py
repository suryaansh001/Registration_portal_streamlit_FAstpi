import streamlit as st
import requests
import os

# The FastAPI webhook server (replace with your actual URL)
FASTAPI_SERVER_URL = os.environ.get('FASTAPI_SERVER_URL', 'http://localhost:8000')

# Streamlit form to get user input
def create_payment_order():
    st.title("RoboSoccer Registration")
    
    # Form to collect user data
    with st.form(key='payment_form'):
        name = st.text_input('Name')
        email = st.text_input('Email')
        college = st.text_input('College')
        amount = 300
        submit_button = st.form_submit_button("Generate Payment Link")

        if submit_button:
            if not name or not email:
                st.error("Please enter both name and email")
                return

            # Send data to FastAPI to generate Razorpay order
            response = requests.post(f'{FASTAPI_SERVER_URL}/create-order', json={
                "name": name,
                "email": email,
                "amount": amount
            })
            
            if response.status_code == 200:
                order_data = response.json()
                razorpay_order_id = order_data.get("razorpay_order_id")
                payment_link = order_data.get("payment_link")

                if razorpay_order_id and payment_link:
                    st.success("Payment Order Created!")
                    st.write(f"**Payment Link**: [Click Here to Pay]({payment_link})")
                    st.write(f"**Razorpay Order ID**: {razorpay_order_id}")
                else:
                    st.error("Failed to create order, please try again.")
            else:
                st.error("Failed to create Razorpay order. Please try again.")
        
# Run the payment order form
create_payment_order()
