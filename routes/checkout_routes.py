from flask import request, jsonify, redirect
import os
from dotenv import load_dotenv
from __main__ import app
import stripe

load_dotenv()
stripe_api_key = os.getenv('stripe_api_key')
stripe.api_key = stripe_api_key


@app.route('/api/create-checkout-session', methods=['POST'])
def create_payment():
    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(request.json.get("amount")),
            currency='cad',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

