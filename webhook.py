from flask import Flask, request, jsonify
import razorpay
import sqlite3
import hmac
import hashlib

app = Flask(__name__)

# Razorpay Secret for Webhook Verification
RAZORPAY_KEY_SECRET = "your_key_secret"

@app.route("/webhook", methods=["POST"])
def razorpay_webhook():
    payload = request.get_data()
    signature = request.headers.get("X-Razorpay-Signature")

    # Verify signature
    expected_signature = hmac.new(
        RAZORPAY_KEY_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()

    if signature != expected_signature:
        return jsonify({"error": "Invalid signature"}), 400

    event = request.json
    if event["event"] == "payment.captured":
        email = event["payload"]["payment"]["entity"]["email"]

        # ✅ Mark user as "Paid" in the database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status='Paid' WHERE email=?", (email,))
        conn.commit()
        conn.close()

    return jsonify(success=True)

if __name__ == "__main__":
    app.run(port=5000)
