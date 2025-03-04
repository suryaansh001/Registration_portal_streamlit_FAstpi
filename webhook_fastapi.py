from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import razorpay
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Razorpay credentials
RAZORAPAY_KEY = os.environ['RAZORPAY_KEY']
RAZORAPAY_SECRET_KEY = os.environ['RAZORPAY_SECRET']
razorpay_client = razorpay.Client(auth=(RAZORAPAY_KEY, RAZORAPAY_SECRET_KEY))

@app.post("/create-order")
async def create_order(request: Request):
    """Generate Razorpay order"""
    data = await request.json()
    
    name = data.get("name")
    email = data.get("email")
    amount = data.get("amount")
    
    if not name or not email or not amount:
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Convert amount to paise (Razorpay expects the amount in paise)
    amount_in_paise = int(amount * 100)

    # Create Razorpay order
    try:
        order = razorpay_client.order.create({
            'amount': amount_in_paise,
            'currency': 'INR',
            'payment_capture': '1',
            'notes': {'user_name': name, 'user_email': email}
        })
        
        # Generate payment link using Razorpay's API (optional)
        payment_link = razorpay_client.payment_link.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "description": "Payment for Order",
            "email": email
        })

        razorpay_order_id = order.get("id")
        payment_link_url = payment_link.get("short_url")

        return JSONResponse({
            "razorpay_order_id": razorpay_order_id,
            "payment_link": payment_link_url
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Here your existing webhook endpoint would go as described earlier
@app.post("/webhook")
async def handle_webhook(request: Request):
    """Handle Razorpay webhook"""
    # Get the event data (JSON) from the request
    event = await request.json()

    # Get the signature from the request headers
    signature = request.headers.get("X-Razorpay-Signature")
    
    # Verify the signature
    if not verify_signature(event, signature, RAZORAPAY_SECRET_KEY):
        return JSONResponse(status_code=400, content={"status": "Invalid Signature"})
    
    # If the payment was captured, handle the payment
    if event['event'] == 'payment.captured':
        payment_data = event['payload']['payment']['entity']
        payment_id = payment_data['id']
        user_id = payment_data['notes']['user_id']  # Assuming user_id is in the notes
        user_email = payment_data['notes']['email']  # Assuming email is passed in the notes

        # Update payment status in the database
        update_payment_status(payment_id, user_id)

        # Send confirmation email
        send_confirmation_email(user_email, payment_id)
        
        return JSONResponse(content={"status": "success"})
    
    # Handle other events or default response
    return JSONResponse(content={"status": "event not handled"})

# app = FastAPI()

# RAZORAPAY_SECRET_KEY =os.environ['RAZORPAY_KEY'] #= 'rzp_test_1DP5mmOlF5G5aa'

# @qpp.post("/webhook")
# async def webhook(request: Request):
#     secret = os.environ['RAZORPAY_SECRET']
#     #razorapy goves json data
#     signature = await request.json()
#     print(signature)
#     return JSONresponse({'status':'ok'})

# # Razorpay provides a signature in the headers (X-Razorpay-Signature) that you must v
# # erify to ensure the request is coming from Razorpay and hasn't been tampered with.
# # The signature is generated using the HMAC algorithm with SHA256 hash function.
# razorpay_client = razorpay.Client(auth=(RAZORAPAY_KEY, RAZORAPAY_SECRET_KEY))

# def verify_signature(payload,signature,secret_api_key):
#     try:
#         razorpay_client.utility.verify_webhook_signature(payload, signature, secret)
#         return True
#     except razorpay.errors.SignatureVerificationError:
#         return False
#     if event['event'] == 'payment.captured':
#         payment_data = event['payload']['payment']['entity']
#         payment_id = payment_data['id']
#         user_id = payment_data['notes']['user_id'] 
#         update_database(payment_id, user_id)
        
#          # If you added user ID to the Razorpay payment notes
#         # Now, update the database
# def update_database(payment_id, user_id):
#     connection = sqlite3.connect('database.db')
#     cursor = connection.cursor()
#     cursor.execute('UPDATE payments SET status = ? WHERE payment_id = ?', ('PAID', payment_id))
#     connection.commit()
#     connection.close()
# @app.post("/webhook")
# async def handle_webhook(request: Request):
#     event = await request.json()
#     signature = request.headers.get("X-Razorpay-Signature")
    
#     if not verify_signature(event, signature, "YOUR_SECRET_KEY"):
#         return JSONResponse(status_code=400, content={"status": "Invalid Signature"})
    
#     if event['event'] == 'payment.captured':
#         payment_data = event['payload']['payment']['entity']
#         user_id = payment_data['notes']['user_id']  # Assuming user ID was added in the notes
#         update_payment_status(user_id)
#         return JSONResponse(content={"status": "success"})
    
#     return JSONResponse(content={"status": "event not handled"})




